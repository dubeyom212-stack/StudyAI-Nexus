# Hosting StudyAI on PythonAnywhere

This setup runs quizzes without an AI provider. It does not upload local accounts,
practice records, or the Ollama model from your computer.

1. Open a PythonAnywhere Bash console and clone the public repository:

   ```sh
   git clone https://github.com/dubeyom212-stack/StudyAI-Nexus.git ~/StudyAI-Nexus
   cd ~/StudyAI-Nexus
   python3.12 -m venv ~/.virtualenvs/studyai
   ~/.virtualenvs/studyai/bin/pip install -r requirements.txt
   ```

   Use an available Python version of 3.11 or newer. Select that same version in
   the next step. If the folder already exists, inspect and back it up before updating.

2. On **Web**, add a web app with **Manual configuration**. Select the matching
   Python version. Set its virtualenv to `/home/YOUR_USERNAME/.virtualenvs/studyai`.
3. Replace the generated WSGI file's sample application with:

   ```python
   import sys
   sys.path.insert(0, '/home/YOUR_USERNAME/StudyAI-Nexus')
   from pythonanywhere_wsgi import application
   ```

4. Add a static-file mapping from `/static/` to
   `/home/YOUR_USERNAME/StudyAI-Nexus/static`.
5. Turn on **Force HTTPS** and reload the web app.
6. Open the HTTPS address. Create an account, take a quiz, save it, and check its results.

The entry point creates the database and session key under
`~/.local/share/studyai-nexus/`, outside the source folder. Back up that directory
before updates. It defaults to secure session cookies and disabled AI. A local
account is separate from an account on the hosted website.

For later updates, run `git pull --ff-only` inside the source checkout, install
requirements again if they changed, then click **Reload** on the Web page.

Follow [PythonAnywhere's Flask guide](https://help.pythonanywhere.com/pages/Flask)
for hosting-account details. Do not use `flask run` as the public server.
