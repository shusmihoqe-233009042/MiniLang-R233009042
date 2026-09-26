def optimize(tac):

    out = []

    for line in tac:

        parts = line.split()

        if (
            len(parts) == 5
            and parts[1] == "="
            and parts[2].lstrip("-").isdigit()
            and parts[4].lstrip("-").isdigit()
        ):

            a = int(parts[2])
            op = parts[3]
            b = int(parts[4])

            if op == "+":
                value = a + b
            elif op == "-":
                value = a - b
            elif op == "*":
                value = a * b
            elif op == "/":
                if b == 0:
                    out.append(line)
                    continue
                value = a // b
            elif op == "<":
                value = int(a < b)
            elif op == "<=":
                value = int(a <= b)
            elif op == ">":
                value = int(a > b)
            elif op == ">=":
                value = int(a >= b)
            elif op == "==":
                value = int(a == b)
            elif op == "!=":
                value = int(a != b)
            else:
                out.append(line)
                continue

            out.append(f"{parts[0]} = {value}")

        else:
            out.append(line)

    return out
