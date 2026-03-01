import base64
import json
import time
import uuid
from typing import List, Optional

from openai import OpenAI
from playwright.sync_api import Page, sync_playwright
from pydantic import BaseModel, Field


# --- Data Models ---
class SeleniumCommand(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    comment: str = ""
    command: str
    target: str
    targets: List[List[str]] = []
    value: str = ""

class SeleniumTest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    commands: List[SeleniumCommand]

class SeleniumIdeSide(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "2.0"
    name: str
    url: str
    tests: List[SeleniumTest]
    suites: List[dict] = []
    urls: List[str]
    plugins: List[dict] = []

def highlight(page: Page, selector: str):
    try:
        loc = page.locator(selector).first
        loc.wait_for(state="visible", timeout=3000)
        
        original_style = loc.evaluate("""
            el => {
                const old = el.getAttribute('style') || "";
                el.style.border = '5px solid yellow';
                return old;
            }
        """)
        
        time.sleep(1)
        
        loc.evaluate("""
            (el, oldStyle) => {
                if (oldStyle) el.setAttribute('style', oldStyle);
                else el.removeAttribute('style');
            }
        """, original_style)

        time.sleep(0.5)
    except Exception:
        pass

# --- Base Builder (Manual & Simulation) ---
class SeleniumIdeSideBuilder:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.commands = []


    def _execute_command(self, command: str, target: str, value: str) -> bool:
        try:
            selector = target
            if "=" in target:
                prefix, raw = target.split("=", 1)
                if prefix == "id": 
                    selector = f"#{raw}"
                elif prefix == "css": 
                    selector = raw
            
            if command == "open":
                url = self.base_url + target if self.base_url and not target.lower().startswith("http") else target
                self.page.goto(url)
            elif command == "click":
                highlight(self.page, selector)
                self.page.click(selector)
            elif command == "type": 
                highlight(self.page, selector)
                self.page.fill(selector, value)
            return True
        except Exception as e:
            print(f"Error executing {command}: {e}")
            return False

    def play_side(self, side_file: str, name: str = ""):
        print(f"Playing: {side_file} {name}")
        with open(side_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for test in data.get("tests", []):
            for cmd in test.get("commands", []):
                c, t, v = cmd['command'], cmd['target'], cmd['value']
                if self._execute_command(c, t, v):
                    print(f"  Success: {c} {t} {v}")
                else:
                    print(f"  Failed: {c} {t} {v}")

    def save_side(self, filename: str, side: SeleniumIdeSide):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(side.model_dump_json(indent=2))
        print(f"Saved: {filename}")

    def open_url(self, url_or_path: str = "/"):
        url = self.base_url + url_or_path if self.base_url and not url_or_path.lower().startswith("http") else url_or_path
        self.page.goto(url)
        self._add_cmd_to_list("open", url_or_path)

    def _add_cmd_to_list(self, command, target, value=""):
        self.commands.append(SeleniumCommand(command=command, target=target, value=value))

    def close(self):
        self.browser.close()
        self.pw.stop()

# --- AI Extended Builder ---
class AISideBuilder(SeleniumIdeSideBuilder):
    def __init__(self, base_url: str, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(base_url)
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def ai_create_side_file(self, llm_prompt: str, side_file: Optional[str] = None) -> SeleniumIdeSide:
        print(f"AI is thinking to find the steps for: '{llm_prompt}'...")
        screenshot_bytes = self.page.screenshot()
        base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
        
        dom_hint = self.page.evaluate("""() => {
            return Array.from(document.querySelectorAll('input, button, a'))
                .map(el => `<${el.tagName} id="${el.id}" name="${el.name}" class="${el.className}">`).join('\\n');
        }""")

        prompt = f"""
You are a Selenium IDE expert. Return a JSON list of Selenium IDE commands.
[Instruction]: {llm_prompt}
[Current URL]: {self.page.url}
[DOM Hint]: {dom_hint}

Return Format:
{{ "commands": [ {{"command": "click", "target": "id=btn", "value": ""}} ] }}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ],
            }],
            response_format={ "type": "json_object" }
        )

        cmds_data = json.loads(response.choices[0].message.content).get("commands", [])
        selenium_cmds = [SeleniumCommand(**c) for c in cmds_data]

        side = SeleniumIdeSide(
            name=llm_prompt,
            url=self.base_url,
            tests=[SeleniumTest(name=llm_prompt, commands=selenium_cmds)],
            urls=[self.base_url]
        )

        if side_file:
            self.save_side(side_file, side=side)
        return side