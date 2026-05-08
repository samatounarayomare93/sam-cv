import sys
import os

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

def test_cv():
    try:
        from core.cv_playwright_pdf import generate_cv_from_html_playwright
        print("Starting CV generation...")
        path = generate_cv_from_html_playwright()
        if path and os.path.exists(path):
            print(f"SUCCESS: CV generated at {path}")
            print(f"Size: {os.path.getsize(path)} bytes")
        else:
            print("FAILED: CV path is None or does not exist")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cv()
