# Selenium IDE AI Side Builder
Use AI assistance to create Selenium IDE script files interactively, then run them without AI. There's no need to spend time figuring out CSS selectors for Selenium or Playwright scripting.

### Quick Start
* Install uv
* Add the OPENAI_API_KEY to the .env file (if it doesn't exist, create a new one).
* Run the following:
  - builder.py with AI
  - demo1.py without AI

### Use AI assistance to record playwright actions in the Selenium IDE .side format. 

Record login and logout.

```bash
% uv run builder.py --output demo2

[Step 1] AI prompt for browser action [exit]: Log into https://saucedemo.com
Playing: sides\demo2_step_1.side ()
    Success: open https://saucedemo.com
    Success: type id=user-name
    Success: type id=password
    Success: click css=.btn_action
    Save sides\demo2_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Log out
Playing: sides\demo2_step_2.side ()
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
    Save sides\demo2_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]:

Scripts created: demo2_sync.py, demo2_async.py
Side files saved in: sides/
```

### Play the .side files.

Play login and logout with sync or async API.

```bash
% uv run demo2_sync.py
Playing: sides/demo2_step_1.side (Log into https://saucedemo.com)
    Success: open https://saucedemo.com
    Success: type id=user-name
    Success: type id=password
    Success: click css=.btn_action
Playing: sides/demo2_step_2.side (Log out)
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
Done.

% uv run demo2_async.py
Playing (Async): sides/demo2_step_1.side (Log into https://saucedemo.com)
    Success: open https://saucedemo.com
    Success: type id=user-name
    Success: type id=password
    Success: click css=.btn_action
Playing (Async): sides/demo2_step_2.side (Log out)
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
Done.
```
