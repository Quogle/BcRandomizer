import sys, os
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]  # adjust if needed
JAVA_EXE = BASE / "dev" / "dependencies" / "jdk-21" / "bin" / "java.exe"

print("JAVA PATH:", JAVA_EXE)
print("EXISTS:", JAVA_EXE.exists())