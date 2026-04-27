# Registry Fix Checker - Shows corrupted Python registry entries
import subprocess
import sys

print("=" * 70)
print("PYTHON REGISTRY DIAGNOSTIC")
print("=" * 70)
print()

# Check registry for Python 3.11
print("[1] Checking HKLM registry:")
result = subprocess.run(
    ['reg', 'query', r'HKLM\SOFTWARE\Python\PythonCore\3.11\InstallPath'],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print()
print("[2] Checking HKCU registry:")
result2 = subprocess.run(
    ['reg', 'query', r'HKCU\SOFTWARE\Python\PythonCore\3.11\InstallPath'],
    capture_output=True, text=True
)
print(result2.stdout)

print()
print("[3] Python's actual prefix detection:")
import sys
print(f"  sys.prefix: {sys.prefix}")
print(f"  sys.exec_prefix: {sys.exec_prefix}")
print(f"  sys.base_prefix: {sys.base_prefix}")
print(f"  sys.path[0]: {sys.path[0] if sys.path else 'empty'}")

print()
print("=" * 70)
input("Press Enter to exit...")