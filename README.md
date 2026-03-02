# Side Builder and Player

Build and execute Selenium IDE (.side) scripts with AI-powered efficiency.

## Key Features
* **AI-Powered Recording:** Generate `.side` files using natural language. No more manual F12 inspection.
* **Cost-Efficient:** Use AI only for recording; execution is 100% local and free.
* **Standard Format:** Fully compatible with the Selenium IDE (.side) ecosystem.
* **Developer Friendly:** Supports both Sync/Async Playwright and Selenium APIs.
* **Zero-Config Selectors:** AI automatically finds the best ID, CSS, or XPath for you.

## Quick Start

### Installation (via uv)
```bash
git clone https://github.com/tayaee/side-builder.git
cd side-builder
uv tool install -e .
side-builder --help
```

### Running Examples
```
cd examples/saucedemo/login-cart-order-logout
uv run login_cart_order_logout_sync.py
```

## Why Side Builder?
Stop fighting with broken CSS selectors. side-builder bridges the gap between AI-driven intent and browser automation, allowing you to focus on the workflow rather than the HTML structure.

## Prerequisites
* Python 3.10+
* OpenAI API Key (Required only for the recording phase)

## License
This project is licensed under the MIT License.
