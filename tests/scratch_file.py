from pathlib import Path
from core.script_parser import parse_script

SCRIPT_DIR = Path(__file__).resolve().parent

FILE_NAME = SCRIPT_DIR / "bruce_almighty.txt"


with open(FILE_NAME) as f:
    raw = f.read()

lines = parse_script(raw)
characters = sorted(set(l.character for l in lines))
print(characters)
print(len(lines))