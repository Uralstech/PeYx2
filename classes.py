from dataclasses import dataclass

@dataclass
class LangData:
    modules: list
    keywords: list
    imports: list
    command: str

@dataclass
class EditorData:
    font: str
    size: str
    fg: str
    bg: str
    h1: str
    h2: str