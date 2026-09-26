import sys

from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from tac import TACGenerator
from optimizer import optimize
from backend import VM, RuntimeErrorMini


def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py <source.min>")
        return 1

    path = sys.argv[1]

    try:
        source = open(path, encoding="utf-8").read()

    except OSError as e:
        print(f"File error: {e}")
        return 1

    try:
        # Lexical Analysis
        tokens = Lexer(source).tokenize()

        # Syntax Analysis
        tree = Parser(tokens).parse()

        # Semantic Analysis
        sem = SemanticAnalyzer()
        sem.analyze(tree)

        # Three Address Code
        tac = TACGenerator().generate(tree)

        # Optimization
        optimized = optimize(tac)

        print("=== TOKENS ===")
        print(
            " ".join(
                f"{t.kind}:{t.value}"
                for t in tokens
                if t.kind != "EOF"
            )
        )

        print("\n=== TAC ===")
        print("\n".join(tac) or "(empty)")

        print("\n=== OPTIMIZED TAC ===")
        print("\n".join(optimized) or "(empty)")

        print("\n=== EXECUTION ===")
        VM().run(optimized)

        print("\nCompilation and execution successful.")

        return 0

    except (
        LexerError,
        ParserError,
        SemanticError,
        RuntimeErrorMini
    ) as e:

        print(f"\n{e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
