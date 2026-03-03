import json
import os
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from side_player.common import parse_selector_selenium


def highlight(driver: WebDriver, selector_tuple: tuple):
    try:
        wait = WebDriverWait(driver, 3)
        element = wait.until(EC.visibility_of_element_located(selector_tuple))

        original_style = element.get_attribute("style") or ""
        driver.execute_script(
            "arguments[0].style.border = '5px solid yellow';", element
        )

        time.sleep(0.5)

        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);", element, original_style
        )
    except Exception:
        pass


def play_side(driver: WebDriver, side_file: str, name: str = "", base_url: str = "", debug: bool = False):
    if debug:
        print(f"Playing: {side_file} ({name})")
    if not os.path.exists(side_file):
        if debug:
            print(f"    Error: {side_file} not found.")
        return

    with open(side_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for test in data.get("tests", []):
        for cmd in test.get("commands", []):
            c, t, v = cmd["command"], cmd["target"], cmd["value"]
            sel_tuple = parse_selector_selenium(t)

            try:
                if c == "open":
                    url = base_url + t if base_url and not t.startswith("http") else t
                    driver.get(url)

                elif c == "click":
                    highlight(driver, sel_tuple)
                    element = driver.find_element(*sel_tuple)
                    element.click()

                elif c == "type":
                    highlight(driver, sel_tuple)
                    element = driver.find_element(*sel_tuple)
                    element.clear()
                    element.send_keys(v)

                elif c == "setWindowSize":
                    width, height = t.split(",")
                    driver.set_window_size(int(width), int(height))

                if debug:
                    print(f"    Success: {c} {t}")
            except Exception as e:
                if debug:
                    print(f"    Failed: {c} {t} ({e})")
