import base64
import json
import os
import time
from typing import Optional

import click
from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright

from common import SeleniumCommand, SeleniumIdeSide, SeleniumTest
from selenium_ide_sync_player import play_side


class SeleniumIdeSideBuilder:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def save_side(self, filename: str, side: SeleniumIdeSide):
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
        self, llm_prompt: str, side_file: Optional[str] = None
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

SYNC_TEMPLATE = """from playwright.sync_api import sync_playwright
from selenium_ide_sync_player import play_side


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

ASYNC_TEMPLATE = """import asyncio
from playwright.async_api import async_playwright
from selenium_ide_async_player import play_side_async


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


@click.command()
@click.option("--output", default=f"demo_{int(time.time())}", help="Project name")
def main(output):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY not found.")
        return

    sides_dir = "sides"
    if not os.path.exists(sides_dir):
        os.makedirs(sides_dir)

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
            file_path = os.path.join(sides_dir, file_name)

            try:
                builder.ai_create_side_file(llm_prompt=prompt, side_file=file_path)
                play_side(builder.page, file_path)

                if click.confirm(f"    Save {file_path}?", default=True):
                    saved_steps.append((file_path, prompt))
                    step += 1
                elif os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                click.echo(f"    Error: {e}")
    finally:
        builder.close()

    if saved_steps:
        # 1. Sync Code 생성 (현재 디렉토리)
        sync_code = "\n".join(
            [f"        play_side(page, '{f.replace('\\', '/')}', name='{p}')" for f, p in saved_steps]
        )
        sync_filename = f"{output}_sync.py"
        with open(sync_filename, "w", encoding="utf-8") as f:
            f.write(SYNC_TEMPLATE.format(steps=sync_code))

        async_code = "\n".join(
            [
                f"        await play_side_async(page, '{f.replace('\\', '/')}', name='{p}')"
                for f, p in saved_steps
            ]
        )
        async_filename = f"{output}_async.py"
        with open(async_filename, "w", encoding="utf-8") as f:
            f.write(ASYNC_TEMPLATE.format(steps=async_code))

        click.echo(f"\nScripts created: {sync_filename}, {async_filename}")
        click.echo(f"Side files saved in: {sides_dir}/")
    else:
        click.echo("\nNo steps saved.")


if __name__ == "__main__":
    main()
