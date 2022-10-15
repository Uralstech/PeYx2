from dataclasses import dataclass
from re import Pattern

@dataclass
class LangSyntax:
    name: str
    regex: Pattern
    color: str

@dataclass
class LangData:
    syntaxes: list
    command: str

@dataclass
class EditorData:
    font: str
    size: str
    fg: str
    bg: str