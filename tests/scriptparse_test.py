from core.script_parser import ScriptLine, parse_script

def test_parser_basic_scene():
  text = "ROMEO: But soft, what light through yonder window breaks?\nJULIET: O Romeo, wherefore art thou Romeo?\n"
  lines = parse_script(text)

  assert len(lines) == 2
  assert lines[0] == ScriptLine(character="ROMEO", dialogue="But soft, what light through yonder window breaks?")
  assert lines[1].character == "JULIET"

def test_blank_lines():
  text = "\n \n Romeo: Hello\n"
  lines = parse_script(text)
  assert len(lines) == 1

def test_ignores_lines_wo_char():
  text = "(stage direction, no colon)\nROMEO: Hello\n"
  lines = parse_script(text)
  assert len(lines) == 1
  assert lines[0].character == "ROMEO"

def test_all_lowercase():
  text = "juliet: o romeo, wherefore art thou romeo?\n"
  lines = parse_script(text)
  assert len(lines) == 1
  assert lines[0].character == "juliet"  

def test_no_colon():
  text = "Romeo lets run away together juliet\n"
  lines = parse_script(text)
  assert len(lines) == 0
