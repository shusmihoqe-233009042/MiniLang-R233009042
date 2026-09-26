class RuntimeErrorMini(Exception):
    pass


class VM:

    def __init__(self):
        self.vars = {}
        self.arrays = {}
        self.labels = {}
        self.pc = 0

    def value(self, x):

        if x.lstrip("-").isdigit():
            return int(x)

        return self.vars.get(x, 0)

    def run(self, code):

        self.labels = {
            line.split()[1]: i
            for i, line in enumerate(code)
            if line.startswith("LABEL ")
        }

        self.pc = 0

        while self.pc < len(code):

            line = code[self.pc]
            p = line.split()

            if not p:
                self.pc += 1
                continue

            if p[0] == "LABEL":
                self.pc += 1
                continue

            if p[0] == "ARRAY":

                self.arrays[p[1]] = [0] * int(p[2])

                self.pc += 1
                continue

            if p[0] == "PRINT":

                print(self.value(p[1]))

                self.pc += 1
                continue

            if p[0] == "GOTO":

                self.pc = self.labels[p[1]]
                continue

            if p[0] == "IFNZ":

                if self.value(p[1]) != 0:
                    self.pc = self.labels[p[3]]
                else:
                    self.pc += 1

                continue

            if p[0] == "IF":

                left = p[1]
                op = p[2]
                right = p[3]
                label = p[5]

                a = self.value(left)
                b = self.value(right)

                ok = {
                    "==": a == b,
                    "!=": a != b,
                    "<": a < b,
                    "<=": a <= b,
                    ">": a > b,
                    ">=": a >= b
                }[op]

                if ok:
                    self.pc = self.labels[label]
                else:
                    self.pc += 1

                continue

            if p[0] == "BREAK":

                self.pc += 1
                continue

            if "=" in p:

                # Array assignment
                if (
                    len(p) == 6
                    and p[1] == "["
                    and p[3] == "]"
                    and p[4] == "="
                ):

                    arr = p[0]
                    idx = self.value(p[2])
                    val = self.value(p[5])

                    if arr not in self.arrays:
                        raise RuntimeErrorMini(
                            f"unknown array {arr}"
                        )

                    if idx < 0 or idx >= len(self.arrays[arr]):
                        raise RuntimeErrorMini(
                            f"runtime array bounds error: "
                            f"{arr}[{idx}]"
                        )

                    self.arrays[arr][idx] = val

                    self.pc += 1
                    continue

                # Array reading
                if (
                    len(p) == 6
                    and p[1] == "="
                    and p[3] == "["
                    and p[5] == "]"
                ):

                    dest = p[0]
                    arr = p[2]
                    idx = self.value(p[4])

                    if arr not in self.arrays:
                        raise RuntimeErrorMini(
                            f"unknown array {arr}"
                        )

                    if idx < 0 or idx >= len(self.arrays[arr]):
                        raise RuntimeErrorMini(
                            f"runtime array bounds error: "
                            f"{arr}[{idx}]"
                        )

                    self.vars[dest] = self.arrays[arr][idx]

                    self.pc += 1
                    continue

                eq = p.index("=")
                dest = p[0]

                if len(p) == 4:

                    op = p[2]
                    x = self.value(p[3])

                    if op == "-":
                        self.vars[dest] = -x
                    else:
                        self.vars[dest] = x

                    self.pc += 1
                    continue

                if len(p) == 5:

                    a = self.value(p[2])
                    op = p[3]
                    b = self.value(p[4])

                    if op == "/" and b == 0:
                        raise RuntimeErrorMini(
                            "division by zero"
                        )

                    self.vars[dest] = {
                        "+": a + b,
                        "-": a - b,
                        "*": a * b,
                        "/": a // b,
                        "<": int(a < b),
                        "<=": int(a <= b),
                        ">": int(a > b),
                        ">=": int(a >= b),
                        "==": int(a == b),
                        "!=": int(a != b)
                    }[op]

                    self.pc += 1
                    continue

                if len(p) == 3:

                    self.vars[dest] = self.value(p[2])

                    self.pc += 1
                    continue

            raise RuntimeErrorMini(
                f"cannot execute TAC: {line}"
            )
