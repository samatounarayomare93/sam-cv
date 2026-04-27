# Shared launcher wrapper for the main bot entry point
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root))
    try:
        import launch_main_bot
        return launch_main_bot.main()
    except Exception as exc:
        print(f"[ERROR] Isolated launch failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
