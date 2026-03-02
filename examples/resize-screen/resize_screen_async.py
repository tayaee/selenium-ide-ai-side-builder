import asyncio
import time

from playwright.async_api import async_playwright

from side_player.playwright.async_api import play_side_async


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        time.sleep(2)
        await play_side_async(page, "sides/resize_screen_step_1.side", name="Adjust browser size to 500x500")
        time.sleep(2)
        await play_side_async(page, "sides/resize_screen_step_2.side", name="Adjust browser size to 1000x1000")
        time.sleep(2)
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
