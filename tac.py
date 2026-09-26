from ast import *


class TACGenerator:

    def __init__(self):
        self.code = []
        self.temp = 0
        self.label = 0

    def new_temp(self):
        self.temp += 1
        return f"t{self.temp}"

    def new_label(self):
        self.label += 1
        return f"L{self.label}"

    def emit(self, *parts):
        self.code.append(" ".join(map(str, parts)))

    def generate(self, program):
        for s in program.statements:
            self.stmt(s)
        return self.code

    def stmt(self, s):

        if isinstance(s, VarDecl):
            if s.init:
                self.emit(s.name, "=", self.expr(s.init))

        elif isinstance(s, ArrayDecl):
            self.emit("ARRAY", s.name, s.size)

        elif isinstance(s, Assignment):
            val = self.expr(s.expr)

            if s.index is None:
                self.emit(s.name, "=", val)
            else:
                idx = self.expr(s.index)
                self.emit(s.name, "[", idx, "]", "=", val)

        elif isinstance(s, PrintStmt):
            self.emit("PRINT", self.expr(s.expr))

        elif isinstance(s, WhileStmt):

            start = self.new_label()
            body = self.new_label()
            end = self.new_label()

            self.emit("LABEL", start)

            cond = self.expr(s.condition)

            self.emit("IFNZ", cond, "GOTO", body)
            self.emit("GOTO", end)

            self.emit("LABEL", body)

            for x in s.body.statements:
                self.stmt(x)

            self.emit("GOTO", start)
            self.emit("LABEL", end)

        elif isinstance(s, IfStmt):

            then_l = self.new_label()
            end_l = self.new_label()

            cond = self.expr(s.condition)

            self.emit("IFNZ", cond, "GOTO", then_l)

            if s.else_block:
                for x in s.else_block.statements:
                    self.stmt(x)

            self.emit("GOTO", end_l)

            self.emit("LABEL", then_l)

            for x in s.then_block.statements:
                self.stmt(x)

            self.emit("LABEL", end_l)

        elif isinstance(s, SwitchStmt):

            end = self.new_label()

            expr = self.expr(s.expr)

            case_labels = [
                (c.value, self.new_label())
                for c in s.cases
            ]

            default_l = self.new_label() if s.default else end

            for value, label in case_labels:
                self.emit(
                    "IF", expr, "==", value,
                    "GOTO", label
                )

            self.emit("GOTO", default_l)

            for c, (_, label) in zip(
                s.cases, case_labels
            ):

                self.emit("LABEL", label)

                for x in c.statements:
                    self.stmt(x)

                self.emit("GOTO", end)

            if s.default:

                self.emit("LABEL", default_l)

                for x in s.default:
                    self.stmt(x)

                self.emit("GOTO", end)

            self.emit("LABEL", end)

        elif isinstance(s, Block):

            for x in s.statements:
                self.stmt(x)

        elif isinstance(s, BreakStmt):
            self.emit("BREAK")

    def expr(self, e):

        if isinstance(e, Number):
            return str(e.value)

        if isinstance(e, Variable):
            return e.name

        if isinstance(e, ArrayAccess):

            idx = self.expr(e.index)

            t = self.new_temp()

            self.emit(
                t, "=", e.name, "[", idx, "]"
            )

            return t

        if isinstance(e, Unary):

            x = self.expr(e.expr)

            t = self.new_temp()

            self.emit(t, "=", e.op, x)

            return t

        if isinstance(e, Binary):

            a = self.expr(e.left)
            b = self.expr(e.right)

            t = self.new_temp()

            self.emit(t, "=", a, e.op, b)

            return t

        raise ValueError(f"Unknown expression: {e}")
