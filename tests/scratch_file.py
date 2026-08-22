from pathlib import Path
from core.script_parser import parse_script,  main_character

SCRIPT_DIR = Path(__file__).resolve().parent

FILE_NAME = SCRIPT_DIR / "bruce_almighty.txt"


with open(FILE_NAME) as f:
    raw = f.read()

lines = parse_script(raw)
print(main_character(lines, min_lines=3))