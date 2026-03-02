# Install uv (Windows)
```
% powershell -ExecutionPolicy Bypass -c "iwr https://astral.sh/uv/install.ps1 -useb | iex"
```

# Set OpenAI API Key
The Side Builder requires an OpenAI API key to use the gpt-5-nano model.
```
% set OPENAI_API_KEY=sk-proj-OlHCz-hz<redacted>
```

# Clone side-builder
```
% git clone https://github.com/tayaee/side-builder.git
% cd side-builder
% uv tool install -e .
```

# Record *.side scripts
```
% cd examples\saucedemo\login-logout
% side-builder --output login_cart_order_logout
Using OPENAI_API_KEY=sk-proj-OlHCz-hz******************************

[Step 1] AI prompt for browser action [exit]: Go to the home of https://saucedemo.com
Playing: sides\login_cart_order_logout_step_1.side ()
    Success: open https://saucedemo.com
    Save sides\login_cart_order_logout_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Log in
Playing: sides\login_cart_order_logout_step_2.side ()
    Success: type id=user-name
    Success: type id=password
    Success: click id=login-button
    Save sides\login_cart_order_logout_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]: Add a backpack to the cart
Playing: sides\login_cart_order_logout_step_3.side ()
    Success: click id=add-to-cart-sauce-labs-backpack
    Save sides\login_cart_order_logout_step_3.side? [Y/n]:

[Step 4] AI prompt for browser action [exit]: Add a jacket to the cart
Playing: sides\login_cart_order_logout_step_4.side ()
    Success: click css=#add-to-cart-sauce-labs-fleece-jacket
    Save sides\login_cart_order_logout_step_4.side? [Y/n]:

[Step 5] AI prompt for browser action [exit]: Click the cart on the right top corner
Playing: sides\login_cart_order_logout_step_5.side ()
    Success: click css=.shopping_cart_link
    Save sides\login_cart_order_logout_step_5.side? [Y/n]:

[Step 6] AI prompt for browser action [exit]: Remove backpack
Playing: sides\login_cart_order_logout_step_6.side ()
    Success: click id=remove-sauce-labs-backpack
    Save sides\login_cart_order_logout_step_6.side? [Y/n]:

[Step 7] AI prompt for browser action [exit]: Click Checkout
Playing: sides\login_cart_order_logout_step_7.side ()
    Success: click css=.btn_action.btn_medium.checkout_button
    Save sides\login_cart_order_logout_step_7.side? [Y/n]:

[Step 8] AI prompt for browser action [exit]: Enter John as first name, Doe as last name, 11111 as zip code and click Continue
Playing: sides\login_cart_order_logout_step_8.side ()
    Success: type id=first-name
    Success: type id=last-name
    Success: type id=postal-code
    Success: click id=continue
    Save sides\login_cart_order_logout_step_8.side? [Y/n]:

[Step 9] AI prompt for browser action [exit]: Click Finish
Playing: sides\login_cart_order_logout_step_9.side ()
    Success: click id=finish
    Save sides\login_cart_order_logout_step_9.side? [Y/n]:

[Step 10] AI prompt for browser action [exit]: Click Back Home
Playing: sides\login_cart_order_logout_step_10.side ()
    Success: click id=back-to-products
    Save sides\login_cart_order_logout_step_10.side? [Y/n]:

[Step 11] AI prompt for browser action [exit]: Log out
Playing: sides\login_cart_order_logout_step_11.side ()
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
    Save sides\login_cart_order_logout_step_11.side? [Y/n]:

[Step 12] AI prompt for browser action [exit]:

Scripts created: login_cart_order_logout_sync.py, login_cart_order_logout_async.py, login_cart_order_logout_sel_sync.py
Side files saved in: sides/
```

# Replay the sides/*.side with Playwright Sync API
```
% uv run login_cart_order_logout_sync.py
```

# Replay the sides/*.side with Playwright Async API
```
% uv run login_cart_order_logout_async.py
```

# Replay the sides/*.side with Selenium Sync API
```
% uv run login_cart_order_logout_sel_sync.py
```
