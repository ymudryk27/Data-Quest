from __future__ import annotations
import io
import sys
import traceback
from types import MappingProxyType

SAFE_BUILTINS = MappingProxyType({
    "abs": abs,
    "all": all,
    "any": any,
    "enumerate": enumerate,
    "len": len,
    "max": max,
    "min": min,
    "range": range,
    "sum": sum,
    "map": map,
    "filter": filter,
    "zip": zip,
    "sorted": sorted,
})


def evaluate_solution(user_code: str, challenge: dict) -> tuple[bool, str]:
    g = {"__builtins": SAFE_BUILTINS}
    l = {}
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        compiled = compile(user_code, filename="user_code.py", mode="exec")
        exec(compiled, g, l)
        # run tests with user namespace
        ok, msg = challenge["tests"](g, l)
        out = buf.getvalue()
        if out:
            msg += "\n[stdout]\n" + out
        return ok, msg
    except AssertionError as e:
        return False, f"Assertion failed: {e}"
    except Exception as e:
        return False, f"Runtime error: {e}\n" + traceback.format_exc()
    finally:
        sys.stdout = old