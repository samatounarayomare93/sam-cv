import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    site = root / "pydeps" / "Lib" / "site-packages"

    # Force project and vendored dependencies to the front for embedded runtimes.
    sys.path.insert(0, str(root))
    if site.exists() and sys.platform == "win32":
        sys.path.insert(0, str(site))

    import main_bot
    main_bot.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
