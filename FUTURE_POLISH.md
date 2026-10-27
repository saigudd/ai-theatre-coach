# AI Theatre Coach — Future Polish and Roadmap

This file collects product ideas, engineering improvements, milestone progress, and
new problems discovered while testing. Older ideas stay near the top. Completed
milestones and newly discovered work are added below them instead of being inserted
above the existing notes.

## UI and demo-experience backlog

### Near-term usability

- [x] Show active script, actor, current cue, basic progress, and transcript.
- [x] Show a loading spinner during AI generation.
- [ ] Improve transcript scanning and distinguish script text from generated text.
- [ ] Allow previous dialogue to be collapsed or expanded.
- [ ] Improve visible recovery actions when AI generation fails.
- [ ] Add clearer empty, parsing, complete, and paused states.
- [ ] Validate keyboard and mobile-width usability.

### Visual identity — later polish

- [ ] Develop a restrained rehearsal-room or theatre-stage visual direction.
- [ ] Consider character cards and richer progress visualization.
- [ ] Support dark-mode contrast and accessibility.
- [ ] Consider a subtle curtain-opening transition only if it does not slow setup.
- [ ] Consider scene-context backgrounds only with clear generation cost, loading,
  accessibility, and distraction controls.
- [ ] Add microphone animation only as functional voice-state feedback.

Decorative work should follow usability and reliability. A recruiter demo benefits
more from obvious state, predictable controls, and recoverable errors than from
animation alone.

## Longer-term product ideas

These are ideas to validate, not committed milestones.

### Memorization tools

- Flashcards and missing-line practice
- Multiple-choice recall and adaptive difficulty
- Timing feedback and memorization progress

### Character exploration

- Character objectives, relationships, conflict, and emotional state
- Alternate interpretations and relevant historical/social context
- Guided questions that help the actor form their own interpretation

### Improv and warm-ups

- Random scene prompts
- Genre switching and unexpected events
- Creativity and warm-up games kept separate from script rehearsal

### Streaming and conversational presentation

- Streaming text responses
- Adjustable response pace and natural pauses
- A typing/thinking indicator
- Interruption controls, primarily for future voice mode

## Prioritized Engineering Roadmap

### Milestone 3 — Script ingestion and deterministic parser robustness

#### Goal

Let users provide common screenplay files without manually converting every file,
and turn supported files into trustworthy structured scenes and dialogue.

#### Input pipeline

- [ ] Continue supporting UTF-8 `.txt` files.
- [ ] Accept text-based `.pdf` screenplays and extract their text before parsing.
- [ ] Detect empty, corrupt, encrypted, or image-only PDFs and show useful errors.
- [ ] Defer OCR for scanned PDFs until real demand justifies its extra dependencies
  and deployment cost.
- [ ] Add file-size limits and encoding/error handling.
- [ ] Keep file extraction separate from screenplay parsing so each can be tested.

#### Parser behavior

- [ ] Preserve scene headings as explicit boundaries instead of only using the
  first heading as a parsing gate.
- [ ] Recognize qualified character cues such as `JAKE (V.O.)` and `NAME (O.S.)`
  while retaining useful delivery metadata.
- [ ] Keep action lines and transitions such as `CUT TO:` out of dialogue.
- [ ] Handle inline and standalone parentheticals intentionally.
- [ ] Support multiline dialogue and common screenplay formatting variations.
- [ ] Normalize character names without merging genuinely different characters.
- [ ] Produce diagnostics when a file parses suspiciously instead of silently
  returning misleading results.

#### Tests and fixtures

- [ ] Add parser tests for scene boundaries, cue qualifiers, parentheticals,
  transitions, action lines, multiline dialogue, malformed input, and page noise.
- [ ] Add small, original regression fixtures representing real formatting
  problems; do not commit an entire copyrighted screenplay as test data.
- [ ] Test TXT extraction and PDF text extraction separately from parser rules.

The parser should remain deterministic while these rules are expressible and
testable. An LLM parser is not yet justified; it would add cost, latency, and
nondeterminism without removing the need for validation.

### Milestone 4 — Purposeful rehearsal modes

The current generated partner response should not be confused with exact script
delivery. Make the behavior an explicit product choice.

#### Strict script rehearsal

- [ ] Deliver the parsed partner line exactly from the screenplay.
- [ ] Do not call an LLM merely to retrieve a line the parser already knows.
- [ ] Support line reveal, missing-line practice, and optional correctness checks.
- [ ] Keep cursor advancement deterministic.

#### Natural rehearsal

- [ ] Allow controlled paraphrasing or improvisation while staying scene-grounded.
- [ ] Preserve character identity and relationships.
- [ ] Clearly label generated dialogue so users do not mistake it for script text.
- [ ] Evaluate prompts against repeatable scene examples.

#### Acting coach

- [ ] Analyze objectives, conflict, subtext, pacing, and interpretation separately
  from playing the scene partner.
- [ ] Explore emotional consistency, confidence, and delivery without pretending
  that subjective performance has one objectively correct score.
- [ ] Let actors compare attempts and track improvement only after the feedback
  rubric is explainable and repeatable.
- [ ] Avoid presenting subjective acting feedback as an objective score without a
  defensible rubric.
- [ ] Add character backstory, relationship, and alternate-interpretation tools
  only after the core rehearsal modes are reliable.

#### Context strategy

- [ ] Continue using bounded recent conversation history and relevant upcoming
  script lines.
- [ ] Evaluate summarizing older context only when longer rehearsals demonstrate a
  real quality or cost problem.

### Milestone 5 — Public-demo reliability and deployment

- [ ] Add user-friendly invalid-file, parse-failure, and provider-error messages.
- [ ] Add bounded retry/backoff only for errors that are safe to retry.
- [ ] Add structured application logging without recording screenplay text or keys.
- [ ] Track request latency and token/cost usage for development diagnostics.
- [ ] Add GitHub Actions for offline tests and dependency checks.
- [ ] Verify Streamlit Community Cloud configuration and secret handling.
- [ ] Add Docker packaging only if a deployment target requires it.
- [ ] Benchmark parser and rehearsal latency against representative scripts before
  optimizing or adding caches.
- [ ] Test responsive behavior on desktop and mobile-width layouts.
- [ ] Add a short privacy/data-use explanation before a public launch.

Caching AI responses should be evaluated carefully: dialogue and uploaded scripts
may be sensitive, and cache keys can accidentally cross session boundaries.

### Milestone 6 — Persistence and frontend/backend separation

- [ ] Decide which user value actually requires persistence: saved scripts,
  rehearsal history, memorization progress, or favorites.
- [ ] Add a small database only after the required data model is clear.
- [ ] Add authentication only when private saved data makes identity necessary.
- [ ] Extract a framework-independent rehearsal engine before replacing Streamlit.
- [ ] Introduce a separate API/frontend only when Streamlit limits a validated user
  experience; do not migrate merely to make the stack look larger.

Possible long-term progress features include saved scenes, memorized-line tracking,
attempt comparison, and personal rehearsal history.

### Milestone 7 — Voice rehearsal

- [ ] Add speech-to-text actor input.
- [ ] Add clearly identified AI voice output for scene partners.
- [ ] Design hands-free controls, interruption, and response pacing.
- [ ] Measure latency before promising a natural real-time experience.
- [ ] Add microphone state/permission feedback and accessible non-voice controls.

Voice is valuable to the product, but it depends on a reliable rehearsal engine,
clear modes, and stable turn transitions.

## Milestone Progress

### Milestone 1 — Safe startup and offline tests

Completed October 14, 2026.

- [x] Import core modules without loading secrets or constructing an API client.
- [x] Create and reuse the default client on demand; accept fake clients in tests.
- [x] Show setup guidance instead of crashing when the API key is missing.
- [x] Guard manual experiments so pytest collection cannot make paid requests.
- [x] Pin development dependencies and block network access during tests.
- [x] Preserve the original parser/conversation tests and add boundary coverage.
- [x] Ignore local Streamlit secrets and pytest caches.
- [ ] Complete the learning checkpoint with the project author.

### Milestone 2 — Testable rehearsal lifecycle and turn engine

In progress.

#### Completed slice: session lifecycle and state isolation

Completed October 26, 2026.

- [x] Bind each active rehearsal to one script fingerprint and filename.
- [x] Store the active actor, immutable parsed lines, cursor, conversation, prompt,
  and transient error in one `RehearsalSession` object.
- [x] Create a fresh isolated session when another script or actor is started.
- [x] Keep uploaded-script and actor choices as drafts until **Start New Rehearsal**.
- [x] Make Restart preserve script/actor identity while returning to the actor's
  first cue with fresh runtime state.
- [x] Add two-script, actor-switch, draft-isolation, and restart regression tests.
- [x] Add a native Streamlit rehearsal workspace with active-session status,
  current cue, progress, transcript, and grouped restart controls.
- [ ] Complete the learning checkpoint with the project author.

#### Remaining Milestone 2 work

These behaviors belong to the rehearsal engine rather than the parser:

- [ ] Define explicit cursor/turn-transition rules.
- [ ] Prevent or clearly handle actor input when it is another character's turn.
- [ ] Fix end-of-role behavior, including the current `None - idx` failure path.
- [ ] Define what happens after the four-partner-turn generation limit is reached.
- [ ] Preserve recoverable state when an AI partner call fails.
- [ ] Add regression tests for each transition and failure path.
- [ ] Add duplicate-submission protection where Streamlit reruns could repeat work.

Milestone 2 should stop at a reliable, testable rehearsal engine. It should not
expand into PDF extraction or a full parser rewrite.

## New Findings and Decisions

### Real-screenplay finding: Avatar diagnostic file

The author-supplied text screenplay exposed multiple independent behaviors:

- The parser skips qualified cues such as `JAKE (V.O.)` because character-cue
  validation rejects periods before name normalization can remove the qualifier.
- Inline parentheticals can remain inside dialogue.
- Transitions and action text can bleed into dialogue when blank-line formatting is
  inconsistent.
- The nearby `AGENT 1` line is parsed correctly. The different line displayed in
  the transcript was generated by the AI partner, not produced by the parser.

Therefore:

- Parser-format and PDF/TXT input work belongs to Milestone 3.
- Cursor, turn, end-of-role, and provider-failure behavior remains in Milestone 2.
- Exact versus generated partner dialogue belongs to the explicit rehearsal modes
  in Milestone 4.

### Current architectural decisions

- Keep deterministic parsing until evidence shows a specific rule cannot be handled
  reliably with deterministic code.
- Keep AI-specific behavior isolated from script extraction and session lifecycle.
- Prefer small original regression fixtures over committing full third-party
  screenplays.
- Do not add response caching, persistence, authentication, OCR, or a separate web
  stack before their product requirements are clear.
