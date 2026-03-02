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
% side-builder --output login-logout
Using OPENAI_API_KEY=sk-proj-OlHCz-hz<redacted>

[Step 1] AI prompt for browser action [exit]: Go to the home of https://saucedemo.com
Playing: sides\login_logout_step_1.side ()
    Success: open https://saucedemo.com
    Save sides\login_logout_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Log in
Playing: sides\login_logout_step_2.side ()
    Success: type id=user-name
    Success: type id=password
    Success: click id=login-button
    Save sides\login_logout_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]: Log out
Playing: sides\login_logout_step_3.side ()
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
    Save sides\login_logout_step_3.side? [Y/n]:

[Step 4] AI prompt for browser action [exit]:

Scripts created: login_logout_sync.py, login_logout_async.py, login_logout_sel_sync.py
Side files saved in: sides/
```

# Replay the sides/*.side with Playwright Sync API
```
% uv run login_logout_sync.py
```

# Replay the sides/*.side with Playwright Async API
```
% uv run login_logout_async.py
```

# Replay the sides/*.side with Selenium Sync API
```
% uv run login_logout_sel_sync.py
```
