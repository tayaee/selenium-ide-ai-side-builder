import asyncio
import json
import os
from playwright.async_api import Page
from common import parse_selector


async def highlight_async(page: Page, selector: str):
    try:
        loc = page.locator(selector).first
        await loc.wait_for(state="visible", timeout=3000)
        original_style = await loc.evaluate(
            "el => { const old = el.getAttribute('style') || ''; "
            "el.style.border = '5px solid yellow'; return old; }"
        )
        await asyncio.sleep(0.5)
        await loc.evaluate(
            "(el, old) => { if (old) el.setAttribute('style', old); "
            "else el.removeAttribute('style'); }",
            original_style,
        )
    except Exception:
        pass


async def play_side_async(
    page: Page, side_file: str, name: str = "", base_url: str = ""
):
    print(f"Playing (Async): {side_file} ({name})")
    if not os.path.exists(side_file):
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
                    await page.goto(url)
                elif c == "click":
                    await highlight_async(page, sel)
                    await page.click(sel)
                elif c == "type":
                    await highlight_async(page, sel)
                    await page.fill(sel, v)
                print(f"    Success: {c} {t}")
            except Exception as e:
                print(f"    Failed: {c} {t} ({e})")
