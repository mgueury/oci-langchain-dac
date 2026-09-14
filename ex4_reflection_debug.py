"""Run ex4_reflection with an automatic Hulk input and periodic stack dumps."""

import builtins
import faulthandler
import runpy
import sys


answers = iter(("hulk", "quit"))


def debug_input(prompt: str = "") -> str:
    print(prompt, end="", flush=True)
    value = next(answers)
    print(value, flush=True)
    return value


faulthandler.enable(file=sys.stderr)
faulthandler.dump_traceback_later(10, repeat=True, file=sys.stderr)
builtins.input = debug_input

try:
    runpy.run_path("ex4_reflection.py", run_name="__main__")
finally:
    faulthandler.cancel_dump_traceback_later()
