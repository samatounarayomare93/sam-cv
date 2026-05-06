import os
import sys

print("---------------------------------------------------------------")
print("  ?? PROJECT CHRONOS - SETUP WIZARD")
print("---------------------------------------------------------------")
print()
print("This will verify your setup and fix common issues.")
print()

# Check Python version
print(f"Python: {sys.version}")
print()

# Run health check
print("Running health check...")
os.system(f"{sys.executable} health_check.py")
print()

print("---------------------------------------------------------------")
print("  ? Setup complete!")
print("---------------------------------------------------------------")
print()
print("To start the bot:")
print("  1. Double-click START_BOT.bat")
print("  2. Or run: python run.py")
print()
print("For immortal mode (auto-restart on crash):")
print("  1. Double-click IMMORTAL.bat")
print()
