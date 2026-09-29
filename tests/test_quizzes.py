import pytest
from unittest.mock import Mock
import ai_service
from app import create_app
from models import db, QuizAttempt
from quiz_bank import SUBJECTS, question_bank, build_quiz

@pytest.fixture
def quiz_app():
    return create_app(dict(TESTING=True, SECRET_KEY='test', SQLALCHEMY_DATABASE_URI='sqlite://', WTF_CSRF_ENABLED=False))

@pytest.fixture
def client(quiz_app, monkeypatch):
    monkeypatch.setattr(ai_service, 'generate', Mock(side_effect=AssertionError('Quizzes must not call AI')))
    client = quiz_app.test_client()
    client.post('/signup', data=dict(username='Quiz user', email='quiz@example.invalid', password='long-password'))
    return client

def start(client, count=5):
    response = client.post('/quizzes', data={'subject':'AP Biology', 'count':str(count)})
    assert response.status_code == 302
    return response.location

def test_banks_and_lengths():
    for subject in SUBJECTS:
        bank = question_bank(subject)
        assert len(bank) >= 10
        assert len({q['prompt'] for q in bank}) == len(bank)
        for q in bank:
            assert len(set(q['options'])) == 4
            assert q['explanation'] and 0 <= q['correct'] < 4
        for count in (5,10):
            items = build_quiz(subject, count)
            assert len(items) == len({q['prompt'] for q in items}) == count
            for item in items:
                original = next(q for q in bank if q['prompt'] == item['prompt'])
                assert item['options'][item['correct']] == original['options'][original['correct']]
    with pytest.raises(ValueError):
        build_quiz('AP Biology', 20)

def test_answers_hidden_save_and_score(client, quiz_app):
    url = start(client)
    with quiz_app.app_context():
        questions = QuizAttempt.query.one().questions
    page = client.get(url)
    assert questions[0]['explanation'].encode() not in page.data
    assert b'Correct answer' not in page.data
    client.post(url, data={'action':'save','q0':'2'})
    with quiz_app.app_context():
        row = QuizAttempt.query.one()
        assert row.answers == {'0':2} and not row.submitted
    client.post(url, data={'action':'submit','q0':'2'})
    with quiz_app.app_context():
        assert not QuizAttempt.query.one().submitted
    answers = {f'q{i}':str(q['correct']) for i,q in enumerate(questions)}
    client.post(url, data={**answers, 'action':'submit'})
    page = client.get(url)
    assert b'5 / 5' in page.data and questions[0]['explanation'].encode() in page.data
    client.post(url, data={'action':'save','q0':'0'})
    with quiz_app.app_context():
        assert len(QuizAttempt.query.one().answers) == 5

def test_missed_retry_and_access(client, quiz_app):
    url = start(client)
    with quiz_app.app_context():
        questions = QuizAttempt.query.one().questions
    client.post(url, data={f'q{i}':str((q['correct']+1)%4 if i == 0 else q['correct']) for i,q in enumerate(questions)})
    retry = client.post(url+'/retry')
    assert retry.status_code == 302
    with quiz_app.app_context():
        row = db.session.get(QuizAttempt,2)
        assert len(row.questions) == 1 and row.questions[0]['prompt'] == questions[0]['prompt']
        assert not row.submitted and not row.answers
    client.post('/logout')
    assert client.get(url).status_code == 302
    client.post('/signup', data=dict(username='Other user', email='other@example.invalid', password='long-password'))
    assert client.get(url).status_code == 404
    assert client.post(url+'/retry').status_code == 404

def test_bad_inputs_and_coverage(client):
    for data in [{'subject':'Unknown','count':'5'}, {'subject':'AP Biology','count':'999'}, {'subject':'AP Biology','count':'no'}, {'subject':'AP Biology','topic':'Made up','count':'5'}]:
        assert client.post('/quizzes', data=data).status_code == 400
    url = start(client)
    assert client.post(url, data={'q0':'9'}).status_code == 400
    assert client.post(url+'/retry').status_code == 400
    for subject in SUBJECTS:
        assert client.get('/quizzes', query_string={'subject':subject}).status_code == 200

def test_hosted_entry_point_uses_private_storage_without_ai(tmp_path, monkeypatch):
    import os
    import runpy
    from pathlib import Path
    for name in ('DATABASE_URL', 'SECRET_KEY', 'AI_PROVIDER', 'COOKIE_SECURE'):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(Path, 'home', lambda: tmp_path)
    # Track environment mutations so pytest restores them after importing the entry point.
    for name in ('DATABASE_URL', 'SECRET_KEY', 'AI_PROVIDER', 'COOKIE_SECURE'):
        monkeypatch.setenv(name, '')
        monkeypatch.delenv(name)
    app = runpy.run_path(str(Path(__file__).parents[1] / 'pythonanywhere_wsgi.py'))['application']
    assert app.config['SESSION_COOKIE_SECURE']
    assert app.config['AI_PROVIDER'] == 'disabled'
    assert (tmp_path / '.local/share/studyai-nexus/studyai.db').exists()
    assert app.test_client().get('/').status_code == 200
    with app.app_context():
        assert not ai_service.connection_status()['available']
        with pytest.raises(ai_service.AIUnavailable, match='Quizzes & tests'):
            ai_service.generate(ai_service.TutorReply, 'test', {})
