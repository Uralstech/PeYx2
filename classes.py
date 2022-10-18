from dataclasses import dataclass
from re import Pattern
from typing import Union

@dataclass
class LangSyntax:
    name: str
    regex: Pattern
    color: str

    sub_syntaxes: Union[list, None]

@dataclass
class LangData:
    syntaxes: list[LangSyntax]
    syntax_tags: list[str]
    command: str

@dataclass
class EditorData:
    font: str
    size: str
    fg: str
    bg: str