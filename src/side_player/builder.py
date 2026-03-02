import base64
import json
import os
import time
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright

from side_player.common import SeleniumCommand, SeleniumIdeSide, SeleniumTest
from side_player.playwright.sync_api import play_side


class SeleniumIdeSideBuilder:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=False)
        self.page = self.browser.new_page()        

    def save_side(self, filename: os.PathLike, side: SeleniumIdeSide):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(side.model_dump_json(indent=2))

    def close(self):
        self.browser.close()
        self.pw.stop()


class AISideBuilder(SeleniumIdeSideBuilder):
    def __init__(self, base_url: str, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(base_url)
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def ai_create_side_file(
        self,
        llm_prompt: str,
        side_file: Optional[os.PathLike] = None,
    ) -> SeleniumIdeSide:
        screenshot_bytes = self.page.screenshot()
        base64_image = base64.b64encode(screenshot_bytes).decode("utf-8")

        dom_hint = self.page.evaluate("""() => {
            return Array.from(document.querySelectorAll('input, button, a'))
                .map(el => `<${el.tagName} id="${el.id}" name="${el.name}" class="${el.className}">`).join('\\n');
        }""")

        prompt = f"""
        You are a Selenium IDE expert. Return a JSON list of Selenium IDE commands.
        
        [Instruction]: {llm_prompt}
        [Current URL]: {self.page.url}
        [DOM Hint]: {dom_hint}
        
        [Selector Rules]:
        - For ID: use "id=element_id"
        - For Class: use "css=.class_name"
        - For Name: use "name=element_name"
        - For XPath: use "xpath=//tag[@attr='val']"
        - NEVER use "class=" as a prefix. Use "css=." instead.
        
        Return Format: {{ "commands": [ {{"command": "click", "target": "css=.shopping_cart_link", "value": ""}} ] }}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
        )

        cmds_data = json.loads(response.choices[0].message.content).get("commands", [])
        selenium_cmds = [SeleniumCommand(**c) for c in cmds_data]

        side = SeleniumIdeSide(
            name=llm_prompt,
            url=self.base_url,
            tests=[SeleniumTest(name=llm_prompt, commands=selenium_cmds)],
            urls=[self.base_url],
        )

        if side_file:
            self.save_side(side_file, side=side)
        return side


# --- Templates for Code Generation ---

PLAYWRIGHT_SYNC_TEMPLATE = """from playwright.sync_api import sync_playwright

from side_player.playwright.sync_api import play_side


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
{steps}
        browser.close()
        print("Done.")


if __name__ == "__main__":
    main()
"""

PLAYWRIGHT_ASYNC_TEMPLATE = """import asyncio

from playwright.async_api import async_playwright

from side_player.playwright.async_api import play_side_async


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
{steps}
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
"""

SELENIUM_SYNC_TEMPLATE = """from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from side_player.selenium.sync_api import play_side


def main():
    chrome_options = Options()
    prefs = {{
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--disable-features=SafeBrowsingPasswordProtection")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.use_automation_extension = False
    driver = webdriver.Chrome(options=chrome_options)
    try:
{steps}
    finally:
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    main()
"""


@click.command()
@click.option(
    "--output", default=f"demo_{int(time.time())}", help="Project name (e.g.: demo1)"
)
def main(output):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY not found.")
        return
    print(f"Using OPENAI_API_KEY={api_key[:16]}******************************")

    sides_dir = Path("sides")
    sides_dir.mkdir(parents=True, exist_ok=True)

    builder = AISideBuilder(base_url="", api_key=api_key)
    saved_steps = []
    step = 1

    try:
        while True:
            prompt = click.prompt(
                f"\n[Step {step}] AI prompt for browser action", default="exit"
            )
            if prompt.lower() in ["exit", "done"]:
                break

            file_name = f"{output}_step_{step}.side"
            file_path = sides_dir / file_name

            try:
                builder.ai_create_side_file(llm_prompt=prompt, side_file=file_path)
                play_side(builder.page, file_path)

                if click.confirm(f"    Save {file_path}?", default=True):
                    saved_steps.append((file_path, prompt))
                    step += 1
                elif file_path.exists():
                    file_path.unlink()
            except Exception as e:
                click.echo(f"    Error: {e}")
    finally:
        builder.close()

    if saved_steps:
        # Generate playwright sync code
        sync_code = "\n".join(
            [
                f"        play_side(page, '{f.as_posix()}', name='{p}')"
                for f, p in saved_steps
            ]
        )
        sync_filename = f"{output}_sync.py"
        with open(sync_filename, "w", encoding="utf-8") as f:
            f.write(PLAYWRIGHT_SYNC_TEMPLATE.format(steps=sync_code))

        # Generate playwright async code
        async_code = "\n".join(
            [
                f"        await play_side_async(page, '{f.as_posix()}', name='{p}')"
                for f, p in saved_steps
            ]
        )
        async_filename = f"{output}_async.py"
        with open(async_filename, "w", encoding="utf-8") as f:
            f.write(PLAYWRIGHT_ASYNC_TEMPLATE.format(steps=async_code))

        # Generate selenium sync code
        sel_sync_code = "\n".join(
            [
                f"        play_side(driver, '{f.as_posix()}', name='{p}')"
                for f, p in saved_steps
            ]
        )
        sel_sync_filename = f"{output}_sel_sync.py"
        with open(sel_sync_filename, "w", encoding="utf-8") as f:
            f.write(SELENIUM_SYNC_TEMPLATE.format(steps=sel_sync_code))

        click.echo(
            f"\nScripts created: {sync_filename}, {async_filename}, {sel_sync_filename}"
        )
        click.echo(f"Side files saved in: {sides_dir.as_posix()}/")
    else:
        click.echo("\nNo steps saved.")


if __name__ == "__main__":
    main()
