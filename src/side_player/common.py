import uuid

from pydantic import BaseModel, Field


class SeleniumCommand(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    comment: str = ""
    command: str
    target: str
    targets: list[list[str]] = []
    value: str = ""


class SeleniumTest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    commands: list[SeleniumCommand]


class SeleniumIdeSide(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "2.0"
    name: str
    url: str
    tests: list[SeleniumTest]
    suites: list[dict] = []
    urls: list[str]
    plugins: list[dict] = []


def parse_selector(target: str) -> str:
    # Convert Selenium IDE target strings to Playwright selectors
    if "=" in target:
        prefix, raw = target.split("=", 1)
        if prefix == "id":
            return f"#{raw}"
        if prefix == "css":
            return raw
        if prefix == "name":
            return f'[name="{raw}"]'
        if prefix == "xpath":
            return f"xpath={raw}"
    return target


def parse_selector_selenium(target: str) -> tuple:
    # Convert Selenium IDE target strings to Selenium locator tuples (By, value)
    from selenium.webdriver.common.by import By

    if "=" in target:
        prefix, raw = target.split("=", 1)
        if prefix == "id":
            return (By.ID, raw)
        if prefix == "css":
            return (By.CSS_SELECTOR, raw)
        if prefix == "name":
            return (By.NAME, raw)
        if prefix == "xpath":
            return (By.XPATH, raw)
    # Default to CSS selector if no prefix
    return (By.CSS_SELECTOR, target)
