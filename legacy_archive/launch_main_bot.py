"""Launcher compatibility shim for legacy tests and scripts."""

import os
import sys

import main_bot


class _PatchablePath(list):
    """List subclass so unittest can patch .insert on Python 3.14."""


if not isinstance(sys.path, _PatchablePath):
    sys.path = _PatchablePath(sys.path)


def main() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    core_path = os.path.join(root, "core")
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
    main_bot.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
