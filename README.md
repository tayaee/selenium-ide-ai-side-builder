# Selenium IDE AI Side Builder

### Quick Start
* Install uv
* Add the OPENAI_API_KEY to the .env file (if it doesn't exist, create a new one).
* Run the following:
  - builder.py with AI
  - demo1.py without AI

### Use AI assistance to record playwright actions in the Selenium IDE .side format. 
```bash
% uv run builder.py --output demo1
--- Designer Mode: demo1 ---

[Step 1] Action (or 'exit') [exit]: Go to https://saucedemo.com
Task: 'Go to https://saucedemo.com'...
Saved: demo1_step_1.side
Playing: demo1_step_1.side 
  Success: open https://saucedemo.com 
Save demo1_step_1.side? [Y/n]: 

[Step 2] Action (or 'exit') [exit]: Log in
Task: 'Log in'...
Saved: demo1_step_2.side
Playing: demo1_step_2.side
  Success: type id=user-name standard_user
  Success: type id=password secret_sauce
  Success: click id=login-button
Save demo1_step_2.side? [Y/n]:

[Step 3] Action (or 'exit') [exit]: Add a backpack to cart
Task: 'Add a backpack to cart'...
Saved: demo1_step_3.side
Playing: demo1_step_3.side
  Success: click id=add-to-cart-sauce-labs-backpack
Save demo1_step_3.side? [Y/n]:

[Step 4] Action (or 'exit') [exit]: Click cart on the right top corner
Task: 'Click cart on the right top corner'...
Saved: demo1_step_4.side
Playing: demo1_step_4.side
  Success: click css= .shopping_cart_link
Save demo1_step_4.side? [Y/n]:

[Step 5] Action (or 'exit') [exit]: Remove the backpack from the cart
Task: 'Remove the backpack from the cart'...
Saved: demo1_step_5.side
Playing: demo1_step_5.side
  Success: click id=remove-sauce-labs-backpack
Save demo1_step_5.side? [Y/n]:

[Step 6] Action (or 'exit') [exit]: Click the hamburger menu on the left top corner
Task: 'Click the hamburger menu on the left top corner'...
Saved: demo1_step_6.side
Playing: demo1_step_6.side
  Success: click id=react-burger-menu-btn
Save demo1_step_6.side? [Y/n]:

[Step 7] Action (or 'exit') [exit]: Click Logout
Task: 'Click Logout'...
Saved: demo1_step_7.side
Playing: demo1_step_7.side
  Success: click id=logout_sidebar_link
Save demo1_step_7.side? [Y/n]:

[Step 8] Action (or 'exit') [exit]: exit

--- Process Finished ---
Files: demo1_step_1.side, demo1_step_2.side, demo1_step_3.side, demo1_step_4.side, demo1_step_5.side, demo1_step_6.side, demo1_step_7.side
Script: demo1.py
```

### Play the .side files.
```bash
% uv run demo1.py
Playing: demo1_step_1.side Go to https://saucedemo.com
  Success: open https://saucedemo.com
Playing: demo1_step_2.side Log in
  Success: type id=user-name standard_user
  Success: type id=password secret_sauce
  Success: click id=login-button
Playing: demo1_step_3.side Add a backpack to cart
  Success: click id=add-to-cart-sauce-labs-backpack
Playing: demo1_step_4.side Click cart on the right top corner
  Success: click css= .shopping_cart_link
Playing: demo1_step_5.side Remove the backpack from the cart
  Success: click id=remove-sauce-labs-backpack
Playing: demo1_step_6.side Click the hamburger menu on the left top corner
  Success: click id=react-burger-menu-btn
Playing: demo1_step_7.side Click Logout
  Success: click id=logout_sidebar_link
Done.
```
