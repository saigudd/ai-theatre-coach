- ##UI 

- theatre stage aesthetic
- curtain opening animation
- rehearsal room theme
- character cards
- progress visualization
- microphone animation (future voice mode)
- responsive layout for different screen sizes
- generating a background from the given context of the scene 
- loading screens during AI generation
- error messages when AI fails
- conversation display improvements
- ability to hide/show previous dialogue
- dark mode
- typing indicator while AI is thinking
- mobile-friendly layout

-----------------------------------------------------------------------------------------------------------------
- ##Functions

- ###script intelligence:
      = explains the script/context
      = EX: upload scripts (PDF/TXT), automatically identify characters, extract scenes and dialogue, identitfy relationships
      = GOAL: remove manual setup and make the AI understand the entire play
- ###character intelligence: 
      = explains motivations/relationships
      = EX: character backstory analysis, goals and conflicts, emotional state analysis
      = GOAL: better mental immersion of the character for the actor
- ###scene partner/memorization mode: 
      = continuous dialogue with optional stage directions 
      = EX: flashcards, multiple choice recall, missing line practice, adaptive difficulty, track memorization progress, timing analysis, emotional delievery scoring
      = GOAL: memorize and practice lines.
- ###character exploration mode: 
      = help actor/s better understand their character
      = EX: "Why does your character do this?", alternate interpretations of the character, historical/social analysis
      = GOAL: understand the role.
- ###acting coach/performance evaluation mode:
      = analyze actor's performance
      = EX: emotional consistency, pacing, confidence, delivery, compare attempts, track improvement
      = GOAL: provide measurable acting improvement
- ###improv mode: 
      = help actor/s with practicing their creativity
      = EX: random scene generator, genre switching, unexpected events, warmup games
      = GOAL: build creativity.
- ###streaming responses: 
      = make the ouput have pauses, sort of like a conversation
      = EX: adjustable response speed, natural pauses, interrupt AI mid-response
      = GOAL: better appearance 
- ###actor progress tracking:
      = give ability to measure/see growth
      = EX: save rehearsal history, track memorized scenes, show improvement metrics, store favorite characters/scenes
      = GOAL: create long-term training companion
- ###voice rehearsal:
      = help actor rehearse through actual voice
      = EX: speech-to-text actor input, AI voice responses, hands-free rehearsal
      = GOAL: mirror acutal, real rehearsal experience

-----------------------------------------------------------------------------------------------------------------

##Engineering Roadmap

- unit testing
- response streaming
- structured logging
- token usage analytics
- cost tracking dashboard
- retry/backoff logic
- response caching
- deployment (Streamlit Cloud or Docker)
- CI/CD pipeline (GitHub Actions)
- script parser
- prompt evaluation framework
- performance benchmarking

-----------------------------------------------------------------------------------------------------------------
- ##Problems to fix 

- ###Context-Aware Rehearsal
   - problem: AI = generic without understanding the scene
   - solution: allow user to provide character, scene, etc...
   - future: auto-extract this info from uploaded scripts
   - status: DONE!
- ###Conversation Memory
   - problem: AI responds once and the rehearsal ends.
   - solution: chat history, session state, context management
   - future: maintain convo history so the actor and AI can continue a scene naturally.
   -status: v1 DONE
- ###Prompt Management
   - problem: prompts become difficult to maintain as features increase
   - solution: move prompts into separate files/functions
   - future: test and optimize prompts
   - status: DONE
- ###API Reliability
   - problem: API failures crash the application
   - solution: handle errors 
   - future: retry logic, user-friendly messages
   - status: DONE
- ###Token Optimization
   - problem: long conversations increase API costs
   - solution: limit history and summarize older conversations
   - future: automatic memory compression
   - status: DONE!
- ###Script Grounding
   - problem: AI relies on manually entered context instead of the actual script
   - solution: upload and parse scripts into structured scene information
   - future: automatically identify scenes, characters, dialogue, and relationships
   - status: FUTURE
- ###Voice Interaction
   - problem: typing every line ruins the whole rehearsal immersion
   - solution: speech-to-text and AI voice responses
   - future: full hands-free rehearsal
   - status: FUTURE
- ###Scene Progress-Tracking
   - problem: rehearsals disappear after the session ends
   - solution: save scenes and rehearsal history
   - future: actor dashboard and saved projects
   - status: FUTURE

-----------------------------------------------------------------------------------------------------------------
Engineering Improvements — TODO

- [ ] Build robust screenplay parser
      - ignore scene headings
      - ignore action lines
      - ignore parentheticals
      - normalize character names
      - support multiline dialogue
      - handle common screenplay formatting variations

- [ ] Add strict script rehearsal mode
      - AI follows actual script dialogue
      - prevent unnecessary improvisation
      - preserve exact dialogue when appropriate

- [ ] Add natural scene rehearsal mode
      - allow controlled improvisation
      - maintain character identity
      - respond naturally while remaining grounded in script

- [ ] Add parser test suite
      - standard screenplay
      - parentheticals
      - multiline dialogue
      - scene transitions
      - malformed input

- [ ] Improve script state management
      - current scene
      - current line
      - current speaker
      - scene transitions

- [ ] Improve context management
      - recent conversation history
      - persistent scene context
      - relevant upcoming script lines
      - summarize older context when necessary

- [ ] Add duplicate-submission protection

- [ ] Add loading/progress states

- [ ] Add structured error handling
      - API errors
      - invalid files
      - unsupported formats
      - parsing failures

- [ ] Add token usage / latency tracking

- [ ] Add response caching where appropriate

- [ ] Add automated tests

- [ ] Add deployment configuration

- [ ] Add observability/debug logging