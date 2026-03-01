from playwright.sync_api import sync_playwright
from selenium_ide_sync_player import play_side


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        play_side(page, 'sides/demo2_step_1.side', name='Log into https://saucedemo.com')
        play_side(page, 'sides/demo2_step_2.side', name='Log out')

        browser.close()
        print("Done.")


if __name__ == "__main__":
    main()
