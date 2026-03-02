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
% cd examples\resize-screen
```

# Replay the sides/*.side with Playwright Sync API
```
% uv run resize_screen_sync.py
```

# Replay the sides/*.side with Playwright Async API
```
% uv run resize_screen_async.py
```

# Replay the sides/*.side with Selenium Sync API
```
% uv run resize_screen_sel_sync.py
```
