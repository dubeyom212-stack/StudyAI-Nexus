"""WSGI entry point for a quiz-only PythonAnywhere deployment."""
import os
from pathlib import Path

# Keep private data outside the Git checkout so source updates cannot replace it.
data_dir = Path.home() / '.local' / 'share' / 'studyai-nexus'
data_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('DATABASE_URL', 'sqlite:///' + (data_dir / 'studyai.db').as_posix())
os.environ.setdefault('AI_PROVIDER', 'disabled')
os.environ.setdefault('COOKIE_SECURE', '1')
secret_file = data_dir / 'session-key'
if not os.environ.get('SECRET_KEY'):
    import secrets
    try:
        with secret_file.open('x') as stream:
            stream.write(secrets.token_hex(32))
        secret_file.chmod(0o600)
    except FileExistsError:
        pass
    os.environ['SECRET_KEY'] = secret_file.read_text().strip()

from app import create_app
application = create_app()
