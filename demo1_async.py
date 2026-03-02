import asyncio

from playwright.async_api import async_playwright

from side_player.playwright.async_api import play_side_async


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await play_side_async(page, 'sides/demo1_step_1.side', name='Go to the home of https://saucedemo.com')
        await play_side_async(page, 'sides/demo1_step_2.side', name='Log in')
        await play_side_async(page, 'sides/demo1_step_3.side', name='Add a backpack to the cart')
        await play_side_async(page, 'sides/demo1_step_4.side', name='Go to cart for checkout')
        await play_side_async(page, 'sides/demo1_step_5.side', name='Click Checkout')
        await play_side_async(page, 'sides/demo1_step_6.side', name='Enter John as first name, Doe as last name, 11111 as zip code and click Continue')
        await play_side_async(page, 'sides/demo1_step_7.side', name='Click Finish')
        await play_side_async(page, 'sides/demo1_step_8.side', name='Click Back Home')
        await play_side_async(page, 'sides/demo1_step_9.side', name='Log out')
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
