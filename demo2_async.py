import asyncio
from playwright.async_api import async_playwright
from selenium_ide_async_player import play_side_async


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await play_side_async(page, 'sides/demo2_step_1.side', name='Log into https://saucedemo.com')
        await play_side_async(page, 'sides/demo2_step_2.side', name='Log out')

        await browser.close()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
