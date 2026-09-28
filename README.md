# StudyAI Nexus

**Work through a question. Find the missing step. Try again.**

StudyAI Nexus is an AP study workspace built with Flask. It brings together 26
course topic guides, a local AI tutor, original practice questions, feedback on
written answers, and a notebook of mistakes to revisit.

The interface uses charcoal backgrounds, acid-yellow task panels, and a course
list that keeps the next piece of work within reach.

[Get started](#run-locally) · [Local AI](#free-local-ai-with-ollama) ·
[Configuration](#configuration) · [Troubleshooting](#troubleshooting) ·
[Contributing](#contributing)

## A typical session

1. Create an account and add the AP courses you are taking.
2. Pick a topic and generate a foundation, core, or challenge question.
3. Write your reasoning, using a hint if you need a starting point.
4. Read feedback against three criteria and compare with the reference solution.
5. Return to the mistake notebook or follow your next study-plan task.

You can also ask the tutor to explain a step or check your reasoning. Plans use
recent attempts and optional confidence ratings; they do not predict exam scores.

## Run locally

Requires Python 3.11 or newer and Git. Ollama is needed for local AI; accounts,
course selection, and saved work remain available when AI is offline.

Clone the repository and enter its folder:

```sh
git clone https://github.com/dubeyom212-stack/StudyAI-Nexus.git
cd StudyAI-Nexus
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app:create_app run --port 5055
```

### macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app:create_app run --port 5055
```

Open [localhost:5055](http://127.0.0.1:5055) and create an account. Accounts and work are stored in
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

## Configuration

Set environment variables before starting Flask. The defaults work for a local
Ollama installation:

| Variable | Default | Purpose |
| --- | --- | --- |
| `AI_PROVIDER` | `ollama` | Select `ollama` or `openai`. |
| `OLLAMA_URL` | `http://127.0.0.1:11434` | Address of the local model server. |
| `OLLAMA_MODEL` | `qwen3:4b` | Installed model name, including its tag. |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model used when OpenAI is selected. |
| `OPENAI_API_KEY` | Empty | Required only for the optional OpenAI provider. |
| `DATABASE_URL` | `sqlite:///studyai.db` | Database connection; this SQLite path resolves inside `instance/`. |
| `SECRET_KEY` | Generated locally | Stable session-signing secret for deployment. |
| `COOKIE_SECURE` | Disabled | Set to `1` when serving over HTTPS. |

For example, to select a different model you have already downloaded:

```powershell
$env:OLLAMA_MODEL='your-installed-model:tag'
.\.venv\Scripts\python.exe -m flask --app app:create_app run --port 5055
```

On macOS/Linux, use `export OLLAMA_MODEL='your-installed-model:tag'` before starting
Flask. See [.env.example](.env.example) for a reference. Do not commit private keys
or databases. Keep the same `DATABASE_URL` when restarting to retain access to the
same accounts and saved work.

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

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Local AI is offline | Open Ollama, then use **Check AI connection** in the app footer. Confirm its server address matches `OLLAMA_URL`. |
| Model not downloaded | Run `ollama list`. If the configured model is missing, run `ollama pull qwen3:4b` or download the model named in `OLLAMA_MODEL`. |
| Response takes a long time | Local inference depends on available memory and CPU/GPU. A live generation on a 16 GB development laptop took about 65 seconds; this is an example, not a guarantee. |
| Tutor returns an error | Check the connection, shorten the request, and retry. Submitted practice answers are saved before grading begins. |
| Accounts seem to be missing | Check `DATABASE_URL` and the database in `instance/`. Starting with a different database does not transfer accounts automatically. |
| Port 5055 is occupied | Stop the previous development server or use a different `--port` and open that port in the browser. |

Small local models can produce weak questions or incorrect feedback even when the
connection works. Use class materials and official AP resources to check uncertain
answers. Automated tests verify app behavior, not subject-matter accuracy.

## Project layout

```text
app.py                 Routes, authentication, validation, and app factory
ai_service.py          Ollama/OpenAI adapters and structured response validation
ap_data.py             AP course topic guides
learning.py            Plan priority and topic progress logic
models.py              Accounts, enrollments, attempts, tutor history, usage
templates/            Server-rendered pages
static/               Styles, browser behavior, and local KaTeX assets
tests/                Automated application tests
instance/             Local data and session key (ignored by Git)
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest -q
```

Automated tests mock provider responses to verify account isolation, confidence
validation, course switching, error recovery, provider adapters, conversation
context, feedback persistence, and evidence-based planning. They do not establish
the educational quality of model-generated questions; perform live model checks too.

## Contributing

Keep each update focused and reviewable:

1. Create a branch from the latest `main`.
2. Make one coherent change and update the relevant documentation.
3. Run the tests for behavior changes. Check desktop and mobile layouts for UI changes.
4. Commit with a message describing what changed, then open a pull request.
5. Describe the student-facing behavior, how it was checked, and any remaining limitations.

GitHub Actions runs the test suite on pushes and pull requests. Keep local models,
virtual environments, databases, and secrets out of commits. Changes to AI prompts
also need live examples: passing mocked tests alone does not demonstrate useful
feedback or correct questions.

## References

- [Official AP courses](https://apcentral.collegeboard.org/courses)
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)

Math display uses vendored KaTeX 0.16.22 (MIT license included in static/vendor/katex). Assets are served locally for offline use. Unsafe KaTeX commands are disabled.
