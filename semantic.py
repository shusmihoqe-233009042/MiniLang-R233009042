from ast import *

class SemanticError(Exception):
    pass


class Symbol:
    def __init__(self, kind, size=None):
        self.kind = kind
        self.size = size


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}
        self.errors = []

    def error(self, msg):
        self.errors.append(msg)

    def analyze(self, program):
        for s in program.statements:
            self.stmt(s)

        if self.errors:
            raise SemanticError(
                "\n".join(f"Semantic error: {e}" for e in self.errors)
            )

    def stmt(self, s):

        if isinstance(s, VarDecl):
            if s.name in self.symbols:
                self.error(f"duplicate declaration of '{s.name}'")
            else:
                self.symbols[s.name] = Symbol("int")

                if s.init:
                    self.expr(s.init)

        elif isinstance(s, ArrayDecl):
            if s.name in self.symbols:
                self.error(f"duplicate declaration of '{s.name}'")
            else:
                self.symbols[s.name] = Symbol("array", s.size)

        elif isinstance(s, Assignment):
            sym = self.symbols.get(s.name)

            if not sym:
                self.error(
                    f"assignment to undeclared variable '{s.name}'"
                )

            elif s.index is not None:

                if sym.kind != "array":
                    self.error(
                        f"'{s.name}' is not an array"
                    )

                else:
                    self.check_index(s.index, sym.size)

            elif sym.kind == "array":
                self.error(
                    f"array '{s.name}' needs an index"
                )

            self.expr(s.expr)

        elif isinstance(s, PrintStmt):
            self.expr(s.expr)

        elif isinstance(s, WhileStmt):
            self.expr(s.condition)

            for x in s.body.statements:
                self.stmt(x)

        elif isinstance(s, SwitchStmt):
            self.expr(s.expr)

            seen = set()

            for c in s.cases:

                if c.value in seen:
                    self.error(
                        f"duplicate switch case {c.value}"
                    )

                seen.add(c.value)

                for x in c.statements:
                    self.stmt(x)

            for x in s.default:
                self.stmt(x)

        elif isinstance(s, IfStmt):
            self.expr(s.condition)

            for x in s.then_block.statements:
                self.stmt(x)

            if s.else_block:
                for x in s.else_block.statements:
                    self.stmt(x)

        elif isinstance(s, Block):
            for x in s.statements:
                self.stmt(x)

        elif isinstance(s, BreakStmt):
            pass

    # Array bounds checking
    def check_index(self, idx, size):

        if isinstance(idx, Number):

            if idx.value < 0 or idx.value >= size:
                self.error(
                    f"array index {idx.value} is out of bounds; "
                    f"valid range is 0..{size - 1}"
                )

        self.expr(idx)

    def expr(self, e):

        if isinstance(e, Number):
            return

        if isinstance(e, Variable):
            sym = self.symbols.get(e.name)

            if not sym:
                self.error(
                    f"use of undeclared variable '{e.name}'"
                )

            elif sym.kind == "array":
                self.error(
                    f"array '{e.name}' cannot be used without an index"
                )

        elif isinstance(e, ArrayAccess):

            sym = self.symbols.get(e.name)

            if not sym:
                self.error(
                    f"use of undeclared array '{e.name}'"
                )

            elif sym.kind != "array":
                self.error(
                    f"'{e.name}' is not an array"
                )

            else:
                self.check_index(e.index, sym.size)

        elif isinstance(e, Binary):
            self.expr(e.left)
            self.expr(e.right)

        elif isinstance(e, Unary):
            self.expr(e.expr)
