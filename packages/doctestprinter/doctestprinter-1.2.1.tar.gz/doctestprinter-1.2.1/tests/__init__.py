from pathlib import Path
import sys

sys.path.insert(0, Path(".").resolve())
print("adding", Path(".").resolve())
