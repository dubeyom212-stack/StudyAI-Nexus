# StudyAI Nexus

A Flask study workspace with 26 AP course topic guides, original AI practice,
feedback on student work, a mistake notebook, and a study plan based on attempts.

## Run locally

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app:create_app run --port 5055
```

Open http://127.0.0.1:5055 and create an account. Accounts and work are stored in
`instance/studyai.db`. Existing accounts and old confidence checks are preserved;
new features use additive tables. Back up an existing database before updating.
The previously committed database and bytecode are removed from Git tracking,
not deleted from an existing local checkout by this development workflow.
Do not deploy a clean clone over a production database without preserving it.

## Free local AI with Ollama

1. Install [Ollama for Windows](https://ollama.com/download/windows).
2. Download a model once:

   ```powershell
   ollama pull qwen3:4b
   ```

3. Keep Ollama running on the same computer as Flask. The default server is
   `http://127.0.0.1:11434`. The Windows application normally starts it for you;
   otherwise run `ollama serve`.
4. Start StudyAI. It defaults to `AI_PROVIDER=ollama` and `OLLAMA_MODEL=qwen3:4b`.

The model download is approximately 2.5 GB, separate from the Ollama installation.
Local inference has no API usage fee. It uses the server computer's memory and
CPU/GPU; it does not run on visitors' phones. A small local model can make mistakes,
especially on difficult AP questions. Use a stronger installed model by changing
`OLLAMA_MODEL`. Model licenses apply; review them before redistribution or commercial use.

## Optional paid OpenAI connection

Set these in private server environment settings, not source files:

```text
AI_PROVIDER=openai
OPENAI_API_KEY=<your private API key>
OPENAI_MODEL=gpt-4o-mini
```

API billing is separate from a ChatGPT subscription. The app uses the Responses
API with validated structured outputs and `store=False`. Student questions,
recent turns, and relevant practice feedback are sent to the selected provider.
Names, account emails, and passwords are not included in AI prompts.
`.env.example` is a reference; `.env` files are not automatically loaded.

## What students can do

- Browse/search 26 course topic guides and keep selected courses together.
- Ask a tutor for a hint, explanation, or reasoning check. Recent conversation and
  the latest two practice results for that topic inform the reply.
- Generate an original short-answer question with a hint and a three-criterion
  rubric. The reference solution is only rendered after feedback is received.
- Get feedback citing their work and a concrete correction task. Submitted work
  is saved before the AI call, including when the provider times out.
- Revisit incomplete attempts and mistakes, then try fresh targeted questions.
- Set a session length and optional exam date. Plans prioritize the latest
  unsuccessful attempts, successful topics due for review after three days,
  low-confidence untested topics, then other untested topics.
- See practice evidence separately from optional self-rated confidence.

The exam date is a countdown, not a claim that the whole syllabus fits into the
remaining time. Session durations are suggested time allocations. Course topic
guides are introductory maps, not exhaustive or officially endorsed curricula.
The app does not predict AP exam scores. Generated practice and feedback are
learning aids, not official AP questions or validated grades.

## Reliability and deployment

- No canned AI response is used on provider failure. Errors preserve student work.
- AI output is validated with Pydantic; refusal, malformed output, and timeouts
  show a retry message rather than saving invented results.
- Student records are scoped to their signed-in account. Forms have CSRF
  protection; templates escape model and student content.
- A database-backed per-account hourly request limit bounds routine usage; it is
  not a substitute for gateway rate limiting under adversarial concurrent traffic.
- Set a stable `SECRET_KEY` and `COOKIE_SECURE=1` on an HTTPS deployment. Local
  development creates a private key file in the ignored instance directory.
- Use a production WSGI server with the factory `app:create_app()`, a persistent
  database volume, request limits, and timeouts suitable for local inference.
  Do not expose the Ollama port to the public internet.
- A hosted server needs its own Ollama model or a paid provider connection. This
  computer's local model is not automatically available to a public deployment.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest -q
```

Automated tests mock provider responses to verify account isolation, confidence
validation, course switching, error recovery, provider adapters, conversation
context, feedback persistence, and evidence-based planning. They do not establish
the educational quality of model-generated questions; perform live model checks too.

## References

- [Official AP courses](https://apcentral.collegeboard.org/courses)
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)

Math display uses vendored KaTeX 0.16.22 (MIT license included in static/vendor/katex). Assets are served locally for offline use. Unsafe KaTeX commands are disabled.
