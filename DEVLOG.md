# AI Theatre Coach Development Log

## July 16, 2026
### Milestones Completed

- Created Python project structure.
- Created and activated a virtual environment using venv.
- Installed initial dependencies:
  - streamlit
  - openai
  - python-dotenv
- Created requirements.txt for tracking the required libs
- Initialized Git repository.
- Created .gitignore to protect:
  - venv/
  - .env
  - __pycache__/

### Streamlit Progress

Learned how Streamlit works.
Built first UI:
- Added application title.
- Added text input.
- Added button interaction.
- Learned that Streamlit reruns the script when users interact.

Current prototype:
- User enters a line.
- Button displays the entered line.

### OpenAI Integration
Built first standalone OpenAI API test.

Learned:
- APIs allow programs to communicate with external services.
- API keys authenticate requests.
- Environment variables store sensitive information.
- .env files store environment variables locally.
- python-dotenv loads .env values into the program.

Successfully:
- Sent a request to an LLM.
- Received an AI-generated response.

### Challenges Encountered
- Initially forgot to save files before running.
- Accidentally entered the Python interpreter instead of the terminal.
- Accidentally committed .env and learned how to remove it from Git tracking.
- Learned the difference between Git tracking and .gitignore.

### Next Steps
- Connect OpenAI responses to Streamlit.
- Replace echo response with AI response.
- Begin building actual rehearsal workflow.

----------------------------------------------------------------------------------------------------------------------------------------

## July 20, 2026
### Connected Streamlit with OpenAI

Milestone:
Created the first functional AI interaction.

The application now:
- accepts user input through Streamlit
- creates a prompt
- sends it through OpenAI API
- displays the generated response

Learned:
- Functions control when code executes.
- Returning values allows different parts of an application to communicate.
- APIs require correct method structures.
- Debugging involves reading stack traces and tracing the error location.

Debugging challenge:
Initially used:
client.responses_create()

Fixed by understanding the SDK structure:
client.responses.create()

Result:
AI Line Partner successfully generates acting responses.

----------------------------------------------------------------------------------------------------------------------------------------

## July 22, 2026
# Added Context-Aware Rehearsal Prompting

## Changes Made
Added new user inputs:
- Character name
- Scene context
- Actor's line

Updated the AI prompt to include:
- Character identity
- Scene information
- Actor dialogue
- Response constraints

The AI is now instructed to:
- Stay in character
- Respond only with dialogue
- Avoid stage directions
- Keep responses short and conversational
- Continue the scene naturally

## Testing
Tested with multiple scenarios:

### Odyssey Scene
Before:
- AI produced long dramatic monologues.
- Responses felt more like a narrator.

After:
- AI responded as the character.
- Dialogue became shorter and more suitable for rehearsal.

### Tony Stark / Spider-Man Scene
Tested character-based responses with emotional context.

Learned:
- Providing context significantly improves AI behavior.
- Character relationships and emotional stakes are important for acting responses.

## Engineering Concepts Learned
### Prompt Engineering
Learned that LLM outputs depend heavily on instructions and context.

## Current Limitation
The AI can only respond to one exchange.

A real rehearsal requires:
- conversation history
- memory
- maintaining scene state

Future improvement: Add conversation memory so the actor and AI can continue rehearsing.

----------------------------------------------------------------------------------------------------------------------------------------
## July 25, 2026
### Learned Streamlit Session State

#### Changes
- Built a small Session State experiment.
- Stored a rehearsal counter across reruns.
- Stored a list that persisted between button clicks.

#### Learned
- Streamlit reruns the entire script whenever the user interacts with the app.
- Normal Python variables are recreated every rerun.
- `st.session_state` preserves data across reruns for a user's session.
- Session State can store different data types such as integers and lists.

#### Next Step
Use Session State to maintain conversation history in the AI Theatre Coach.

----------------------------------------------------------------------------------------------------------------------------------------
## August 3, 2026
### Added Multi-Turn Conversation Memory

#### Changes
- Refactored the project into multiple modules.
- Renamed the main.py to `app.py`.
- Moved prompt generation into a dedicated prompts module.
- Moved OpenAI communication into an AI client module.
- Added a ConversationManager class to store conversation history.
- Limited conversation history to a configurable number of turns.
- Added a Clear Scene button to reset the rehearsal.

#### Learned

- Separating UI from business logic makes projects easier to maintain.
- Conversation history must be sent back to the LLM on every request for true multi-turn conversations.
- Session State can store custom Python objects, not just primitive values.
- Organizing code into smaller modules makes future features easier to implement.

#### Testing

Tested several multi-turn conversations.

Observed that:
- The AI remembered previous dialogue.
- Characters stayed consistent throughout the rehearsal.
- Context remained stable across multiple exchanges.

Successfully tested:
- Odyssey rehearsal
- Tony Stark / Spider-Man scene

#### Current Limitation
The AI still relies on manually entered scene information.

Future improvement:
- Upload scripts and automatically extract characters, dialogue, and scene context.

----------------------------------------------------------------------------------------------------------------------------------------