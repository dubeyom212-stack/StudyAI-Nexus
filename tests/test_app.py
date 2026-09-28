from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import ai_service
from app import create_app
from ap_data import ap_topics
from learning import build_plan, topic_status
from models import db, User, Enrollment, PracticeAttempt, TutorTurn, AIUsage

SUBJECT = "AP Calculus AB"
TOPIC = ap_topics[SUBJECT][0]
EXERCISE = dict(prompt="Find the limit of 2x + 1 as x approaches 3. Explain why substitution works.",
                hint="Is the function continuous?", solution="The limit is 7, since linear functions are continuous.",
                rubric=["Uses continuity", "Substitutes x = 3", "Obtains 7"])
FEEDBACK = dict(earned=[True, True, False], evidence=['It is continuous', '2(3)+1', ''], explanation="You substituted correctly but calculated 2(3)+1 as 6.",
                misconception="The final +1 was omitted.", next_step="Recalculate 2(3)+1, writing the multiplication and addition on separate lines.")


@pytest.fixture
def app():
    return create_app(dict(TESTING=True, SECRET_KEY="test-only", SQLALCHEMY_DATABASE_URI="sqlite://",
                           WTF_CSRF_ENABLED=False, OPENAI_API_KEY="", AI_PROVIDER="openai"))


@pytest.fixture
def client(app):
    client = app.test_client()
    client.post('/signup', data=dict(username='Test student', email='test@example.invalid', password='testing-password'))
    return client


@pytest.fixture
def ai(monkeypatch):
    mock = Mock(side_effect=lambda schema, *args: EXERCISE if schema is ai_service.Exercise else
                FEEDBACK if schema is ai_service.Feedback else
                dict(explanation='Use continuity before substitution.', next_step='Substitute x = 3.', check_question='What does 2(3)+1 equal?'))
    monkeypatch.setattr(ai_service, 'generate', mock)
    return mock


def make_attempt(client):
    result = client.post('/practice', data=dict(subject=SUBJECT, topic=TOPIC, difficulty='Core'))
    assert result.status_code == 302
    return result.location


def test_all_pages_and_all_course_topics_render(client):
    for route in ['/', '/courses', '/plan', '/practice', '/tutor', '/mistakes', '/profile', '/galaxy', '/about', '/diagnostic']:
        assert client.get(route).status_code == 200, route
    for subject in ap_topics:
        for route in ['/practice', '/diagnostic', '/galaxy']:
            page = client.get(route, query_string=dict(subject=subject))
            assert page.status_code == 200, (route, subject)
            assert ap_topics[subject][0].encode() in page.data


def test_auth_required(app):
    for route in ['/practice', '/tutor', '/plan', '/courses', '/mistakes', '/profile']:
        assert app.test_client().get(route).status_code == 302


def test_auth_validation_and_duplicates(client, app):
    response = client.post('/signup', data=dict(username='Test student', email='new@example.invalid', password='testing-password'))
    assert b'already in use' in response.data
    response = client.post('/signup', data=dict(username='', email='bad', password='x'))
    assert b'valid email' in response.data
    client.post('/logout')
    assert client.post('/login', data=dict(email='test@example.invalid', password='wrong')).status_code == 200
    assert client.post('/login', data=dict(email='TEST@example.invalid', password='testing-password')).status_code == 302
    with app.app_context():
        assert User.query.count() == 1


def test_csrf_protects_posts_and_logout(app):
    app.config['WTF_CSRF_ENABLED'] = True
    c = app.test_client()
    assert c.post('/signup', data={}).status_code == 400
    assert c.get('/logout').status_code == 405


def test_subject_change_loads_correct_topics(client):
    result = client.get('/practice', query_string=dict(subject='AP Biology', topic=TOPIC))
    assert result.status_code == 200
    assert b'Properties of Water' in result.data
    assert client.post('/practice', data=dict(subject='AP Biology', topic=TOPIC)).status_code == 400
    assert client.get('/practice?subject=invalid').status_code == 400


def test_confidence_is_validated_and_saved(client, app):
    data = dict(subject=SUBJECT, **{f'rating_{i}': 2 for i in range(len(ap_topics[SUBJECT]))})
    assert client.post('/diagnostic', data=data).status_code == 302
    with app.app_context():
        assert Enrollment.query.filter_by(subject=SUBJECT).one().ratings[TOPIC] == 2
    data['rating_0'] = 99
    assert b'Rate every topic' in client.post('/diagnostic', data=data).data


def test_plan_preferences(client, app):
    assert client.post('/plan', data=dict(subject=SUBJECT, minutes=30)).status_code == 302
    assert b'Choose 10' in client.post('/plan', data=dict(subject=SUBJECT, minutes=-5)).data
    assert b'Choose 10' in client.post('/plan', data=dict(subject=SUBJECT, minutes=20, exam_date='2020-01-01')).data
    with app.app_context():
        assert Enrollment.query.filter_by(subject=SUBJECT).one().minutes == 30


def test_practice_feedback_notebook_and_progress(client, app, ai):
    location = make_attempt(client)
    page = client.get(location)
    assert EXERCISE['solution'].encode() not in page.data
    assert client.post(location, data=dict(answer='It is continuous; 2(3)+1 = 6.')).status_code == 302
    page = client.get(location)
    assert b'2/3' in page.data and b'The final +1 was omitted.' in page.data
    assert EXERCISE['solution'].encode() in page.data
    assert b'The final +1 was omitted.' in client.get('/mistakes').data
    assert b'Needs practice' in client.get('/galaxy', query_string=dict(subject=SUBJECT)).data
    assert b'2/3' in client.get('/profile').data
    assert b'Fix the step' in client.get('/').data
    client.post(location, data=dict(answer='Replacement'))
    assert ai.call_count == 2  # No repeated grading of a completed attempt.
    with app.app_context():
        assert PracticeAttempt.query.one().answer.startswith('It is continuous')


def test_owner_isolation(client, app, ai):
    location = make_attempt(client)
    other = app.test_client()
    other.post('/signup', data=dict(username='Other', email='other@example.invalid', password='testing-password'))
    assert other.get(location).status_code == 404
    assert other.post(location, data=dict(answer='stolen')).status_code == 404
    assert b'Find the limit' not in other.get('/profile').data


def test_failed_ai_preserves_answer_and_refunds_limit(client, app, ai):
    location = make_attempt(client)
    ai.side_effect = ai_service.AIUnavailable('Not connected')
    page = client.post(location, data=dict(answer='My unfinished reasoning'))
    assert b'My unfinished reasoning' in page.data and b'Not connected' in page.data
    with app.app_context():
        assert PracticeAttempt.query.one().feedback is None
        assert AIUsage.query.count() == 1


def test_missing_key_never_fakes_response(client, app):
    response = client.post('/tutor', data=dict(subject=SUBJECT, topic=TOPIC, question='Explain continuity', mode='explain'))
    assert b'not connected' in response.data and b'Explain continuity' in response.data
    with app.app_context():
        assert TutorTurn.query.count() == 0


def test_followup_context_and_safe_rendering(client, app, ai):
    data = dict(subject=SUBJECT, topic=TOPIC, question='<script>alert(1)</script>', mode='hint')
    client.post('/tutor', data=data)
    page = client.get('/tutor', query_string=dict(subject=SUBJECT, topic=TOPIC))
    assert b'&lt;script&gt;' in page.data and b'<script>alert' not in page.data
    client.post('/tutor', data=dict(data, question='What happens next?'))
    assert len(ai.call_args.args[3]) == 2
    client.post('/tutor', data=dict(subject='AP Biology', topic=ap_topics['AP Biology'][0], question='What is an enzyme?', mode='explain'))
    assert ai.call_args.args[3] == []


def test_rate_limit_prevents_provider_calls(client, app, ai):
    app.config['AI_HOURLY_LIMIT'] = 1
    make_attempt(client)
    response = client.post('/practice', data=dict(subject=SUBJECT, topic=TOPIC, difficulty='Core'))
    assert b'hourly AI limit' in response.data
    assert ai.call_count == 1


def test_empty_and_oversized_input_does_not_call_ai(client, ai):
    for text in ['', 'x' * 4001]:
        assert client.post('/tutor', data=dict(subject=SUBJECT, topic=TOPIC, question=text, mode='hint')).status_code == 200
    assert ai.call_count == 0


def test_plan_uses_evidence_before_confidence():
    now = datetime.utcnow()
    miss = SimpleNamespace(topic='A', feedback=FEEDBACK, created_at=now)
    passed = SimpleNamespace(topic='B', feedback=dict(FEEDBACK, earned=[True]*3), created_at=now-timedelta(days=4))
    rows = topic_status(['C', 'B', 'A'], [miss, passed], {'C': 1, 'A': 5})
    assert [r['topic'] for r in rows] == ['A', 'B', 'C']
    assert rows[1]['status'] == 'Review due'
    plan = build_plan(rows, 25)
    assert sum(t['minutes'] for t in plan) == 25
    assert plan[0]['instruction'] == FEEDBACK['next_step']


def test_latest_success_supersedes_old_mistake():
    now = datetime.utcnow()
    new = SimpleNamespace(topic='A', feedback=dict(FEEDBACK, earned=[True]*3), created_at=now)
    old = SimpleNamespace(topic='A', feedback=FEEDBACK, created_at=now-timedelta(days=1))
    assert topic_status(['A'], [new, old], {})[0]['status'] == 'On track'


def test_openai_adapter_and_refusal(app, monkeypatch):
    response = SimpleNamespace(status='completed', output_parsed=ai_service.Exercise(**EXERCISE))
    fake = Mock()
    fake.__enter__ = Mock(return_value=fake)
    fake.__exit__ = Mock(return_value=False)
    fake.responses.parse.return_value = response
    monkeypatch.setattr(ai_service, 'OpenAI', Mock(return_value=fake))
    app.config['OPENAI_API_KEY'] = 'test-not-a-real-key'
    with app.app_context():
        assert ai_service.generate(ai_service.Exercise, 'Task', {}) == EXERCISE
        assert fake.responses.parse.call_args.kwargs['store'] is False
        response.output_parsed = None
        with pytest.raises(ai_service.AIUnavailable):
            ai_service.generate(ai_service.Exercise, 'Task', {})


def test_ollama_adapter_and_invalid_output(app, monkeypatch):
    import io
    import json
    app.config['AI_PROVIDER'] = 'ollama'
    response = lambda *a, **kw: io.StringIO(json.dumps({'message': {'content': json.dumps(EXERCISE)}}))
    monkeypatch.setattr(ai_service, 'urlopen', response)
    with app.app_context():
        assert ai_service.generate(ai_service.Exercise, 'Task', {}) == EXERCISE
        monkeypatch.setattr(ai_service, 'urlopen', lambda *a, **kw: io.StringIO('{"bad":1}'))
        with pytest.raises(ai_service.AIUnavailable):
            ai_service.generate(ai_service.Exercise, 'Task', {})


def test_grading_requires_evidence_from_student():
    feedback = dict(FEEDBACK, earned=[True, True, True], evidence=['Invented reasoning', '', '2(3)+1'])
    assert ai_service.grounded_feedback(feedback, '2(3)+1 = 7')['earned'] == [False, False, True]


@pytest.mark.parametrize('prompt', [
    'Write a self-contained original question on biology.',
    'Which of the following is correct?',
    'Find the limit. Hint: factor first.',
])
def test_rejects_incomplete_or_leaked_practice(prompt):
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        ai_service.Exercise(**dict(EXERCISE, prompt=prompt))


def test_connection_status_does_not_claim_offline_ai_is_ready(client, app, monkeypatch):
    from urllib.error import URLError
    app.config['AI_PROVIDER'] = 'ollama'
    monkeypatch.setattr(ai_service, 'urlopen', Mock(side_effect=URLError('offline')))
    assert b'Local AI is offline' in client.get('/connection').data


def test_math_assets_are_available_offline(client):
    for path in ['vendor/katex/katex.min.js', 'vendor/katex/katex.min.css', 'vendor/katex/contrib/auto-render.min.js']:
        assert client.get('/static/' + path).status_code == 200
