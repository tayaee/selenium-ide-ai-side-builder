import uuid
from typing import List
from pydantic import BaseModel, Field


class SeleniumCommand(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    comment: str = ""
    command: str
    target: str
    targets: List[List[str]] = []
    value: str = ""


class SeleniumTest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    commands: List[SeleniumCommand]


class SeleniumIdeSide(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "2.0"
    name: str
    url: str
    tests: List[SeleniumTest]
    suites: List[dict] = []
    urls: List[str]
    plugins: List[dict] = []


def parse_selector(target: str) -> str:
    """Selenium IDE 타겟 문자열을 Playwright 셀렉터로 변환"""
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
