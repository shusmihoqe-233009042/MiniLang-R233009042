from dataclasses import dataclass, field
from typing import Any


@dataclass
class Program:
    statements: list


@dataclass
class Block:
    statements: list


@dataclass
class VarDecl:
    name: str
    init: Any = None


@dataclass
class ArrayDecl:
    name: str
    size: int


@dataclass
class Assignment:
    name: str
    expr: Any
    index: Any = None


@dataclass
class PrintStmt:
    expr: Any


@dataclass
class WhileStmt:
    condition: Any
    body: Block


@dataclass
class SwitchCase:
    value: int
    statements: list


@dataclass
class SwitchStmt:
    expr: Any
    cases: list = field(default_factory=list)
    default: list = field(default_factory=list)


@dataclass
class IfStmt:
    condition: Any
    then_block: Block
    else_block: Block | None = None


@dataclass
class BreakStmt:
    pass


@dataclass
class Binary:
    op: str
    left: Any
    right: Any


@dataclass
class Unary:
    op: str
    expr: Any


@dataclass
class Number:
    value: int


@dataclass
class Variable:
    name: str


@dataclass
class ArrayAccess:
    name: str
    index: Any
