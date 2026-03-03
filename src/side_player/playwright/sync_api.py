import json
import os
import time
from playwright.sync_api import Page
from side_player.common import parse_selector


def highlight(page: Page, selector: str):
    try:
        loc = page.locator(selector).first
        loc.wait_for(state="visible", timeout=3000)
        original_style = loc.evaluate(
            "el => { const old = el.getAttribute('style') || ''; "
            "el.style.border = '5px solid yellow'; return old; }"
        )
        time.sleep(0.5)
        loc.evaluate(
            "(el, old) => { if (old) el.setAttribute('style', old); "
            "else el.removeAttribute('style'); }",
            original_style,
        )
    except Exception:
        pass


def play_side(page: Page, side_file: str, name: str = "", base_url: str = "", debug: bool = False):
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
            sel = parse_selector(t)
            try:
                if c == "open":
                    url = base_url + t if base_url and not t.startswith("http") else t
                    page.goto(url)
                elif c == "click":
                    highlight(page, sel)
                    page.click(sel)
                elif c == "type":
                    highlight(page, sel)
                    page.fill(sel, v)
                elif c == "setWindowSize":
                    width, height = t.split(",")
                    page.set_viewport_size({"width": int(width), "height": int(height)})
                if debug:
                    print(f"    Success: {c} {t}")
            except Exception as e:
                if debug:
                    print(f"    Failed: {c} {t} ({e})")
