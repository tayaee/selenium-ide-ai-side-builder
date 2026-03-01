from selenium_ide_ai_helper import AISideBuilder


def main():
    builder = AISideBuilder(base_url="", api_key="")
    builder.play_side('demo1_step_1.side', name='Go to https://saucedemo.com')
    builder.play_side('demo1_step_2.side', name='Log in')
    builder.play_side('demo1_step_3.side', name='Add a backpack to cart')
    builder.play_side('demo1_step_4.side', name='Click cart on the right top corner')
    builder.play_side('demo1_step_5.side', name='Remove the backpack from the cart')
    builder.play_side('demo1_step_6.side', name='Click the hamburger menu on the left top corner')
    builder.play_side('demo1_step_7.side', name='Click Logout')
    builder.close()
    print("Done.")


if __name__ == "__main__":
    main()
