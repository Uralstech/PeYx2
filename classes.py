from dataclasses import dataclass
from re import Pattern
from typing import Union

@dataclass
class LangSyntax:
    name:  str
    regex: Pattern
    color: str

    sub_syntaxes: Union[list, None]

@dataclass
class LangMetaData:
    version:  str
    online:   str
    download: str
    author:   str
    language: str

@dataclass
class LangData:
    filename:    str
    syntaxes:    list[LangSyntax]
    syntax_tags: list[str]
    command:     str

    metadata:    Union[LangMetaData, None]

@dataclass
class EditorData:
    font: str
    size: str
    fg:   str
    bg:   str