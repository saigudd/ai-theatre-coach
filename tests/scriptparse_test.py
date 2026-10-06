from core.script_parser import ScriptLine, parse_script, main_character

def test_parser_basic_scene():
  text = "INT. ROOM - DAY\nROMEO\nBut soft, what light through yonder window breaks?\n\nJULIET\nO Romeo, wherefore art thou Romeo?\n"
  lines = parse_script(text)

  assert len(lines) == 2
  assert lines[0] == ScriptLine(character="ROMEO", dialogue="But soft, what light through yonder window breaks?")
  assert lines[1].character == "JULIET"

def test_blank_lines():
  text = "INT. ROOM - DAY\n\n \n ROMEO\n Hello\n"
  lines = parse_script(text)
  assert len(lines) == 1

def test_ignores_lines_wo_char():
  text = "INT. ROOM - DAY\n(stage direction, no colon)\nROMEO\n Hello\n"
  lines = parse_script(text)
  assert len(lines) == 1
  assert lines[0].character == "ROMEO"

def test_all_lowercase():
  text = "INT. ROOM - DAY\njuliet\n o romeo, wherefore art thou romeo?\n"
  lines = parse_script(text)
  assert len(lines) == 0

def test_no_colon():
  text = "INT. ROOM - DAY\nRomeo lets run away together juliet\n"
  lines = parse_script(text)
  assert len(lines) == 0

def test_parses_standard_screenplay_cue_format():
  text = (
      "INT. ROOM - DAY\n"
      "                    BRUCE\n"
      "               Oh no, this is bad.\n"
      "                    (sighing)\n"
      "               We need a new plan.\n"
      "\n"
      "          Some description text nobody says out loud.\n"
      "\n"
      "                    ALLY\n"
      "               Relax, it'll be fine.\n"
  )

  lines = parse_script(text)

  assert len(lines) == 2
  assert lines[0].character == "BRUCE"
  assert lines[0].dialogue == "Oh no, this is bad. We need a new plan."
  assert lines[1].character == "ALLY"


def test_main_characters_filters_by_frequency():
    
    lines = [
        ScriptLine(character="BRUCE", dialogue="a"),
        ScriptLine(character="BRUCE", dialogue="b"),
        ScriptLine(character="BRUCE", dialogue="c"),
        ScriptLine(character="RANDOM JUNK", dialogue="x"),
    ]
    assert main_character(lines, min_lines=3) == ["BRUCE"]


def test_ignore_title_page_before_first_scene_heading():
  text = (
    '"THE PLAY"\n'
    "by Someone\n"
    "\n"
    "INT. KITCHEN - DAY\n"
    "\n"
    "                  BRUCE\n"
    "               Hello there.\n"
  )
  lines = parse_script(text)
  assert len(lines) == 1
  assert lines[0].character == "BRUCE"