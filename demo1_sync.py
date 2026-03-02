from playwright.sync_api import sync_playwright

from side_player.playwright.sync_api import play_side


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        play_side(page, 'sides/demo1_step_1.side', name='Go to the home of https://saucedemo.com')
        play_side(page, 'sides/demo1_step_2.side', name='Log in')
        play_side(page, 'sides/demo1_step_3.side', name='Add a backpack to the cart')
        play_side(page, 'sides/demo1_step_4.side', name='Go to cart for checkout')
        play_side(page, 'sides/demo1_step_5.side', name='Click Checkout')
        play_side(page, 'sides/demo1_step_6.side', name='Enter John as first name, Doe as last name, 11111 as zip code and click Continue')
        play_side(page, 'sides/demo1_step_7.side', name='Click Finish')
        play_side(page, 'sides/demo1_step_8.side', name='Click Back Home')
        play_side(page, 'sides/demo1_step_9.side', name='Log out')
        browser.close()
        print("Done.")


if __name__ == "__main__":
    main()
