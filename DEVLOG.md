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

