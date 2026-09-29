"""Instant quiz builder and private, persistent attempts."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models import db, QuizAttempt
from quiz_bank import SUBJECTS, question_bank, build_quiz

quizzes = Blueprint('quizzes', __name__)


@quizzes.route('/quizzes', methods=['GET', 'POST'])
@login_required
def builder():
    subject = request.values.get('subject', SUBJECTS[0])
    if subject not in SUBJECTS:
        if request.method == 'POST':
            abort(400, 'Choose a subject with an available question bank.')
        subject = SUBJECTS[0]
    bank = question_bank(subject)
    topics = sorted({q['topic'] for q in bank})
    # Only offer topic filters with enough distinct items for a five-question quiz.
    filters = [topic for topic in topics if sum(q['topic'] == topic for q in bank) >= 5]
    topic = request.values.get('topic', 'All topics')
    if topic not in ['All topics', *filters]:
        abort(400, 'Choose an available topic.')
    available = sum(topic == 'All topics' or q['topic'] == topic for q in bank)
    if request.method == 'POST':
        try:
            questions = build_quiz(subject, int(request.form.get('count', '5')), topic)
        except (ValueError, TypeError) as exc:
            abort(400, str(exc))
        row = QuizAttempt(user_id=current_user.id, subject=subject, questions=questions, answers={})
        db.session.add(row)
        db.session.commit()
        return redirect(url_for('quizzes.take', quiz_id=row.id))
    history = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.id.desc()).limit(15).all()
    return render_template('quizzes.html', subjects=SUBJECTS, subject=subject, topic=topic,
                           filters=filters, topics=topics, available=available, history=history)


@quizzes.route('/quizzes/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take(quiz_id):
    row = QuizAttempt.query.filter_by(id=quiz_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST' and not row.submitted:
        action = request.form.get('action', 'submit')
        if action not in {'save', 'submit'}:
            abort(400, 'Choose save or submit.')
        answers = {}
        for i in range(len(row.questions)):
            answer = request.form.get(f'q{i}')
            if answer is not None:
                if answer not in {'0', '1', '2', '3'}:
                    abort(400, 'Choose one of the listed answers.')
                answers[str(i)] = int(answer)
        row.answers = answers
        if action == 'submit' and len(answers) != len(row.questions):
            flash('Your selections are saved. Answer every question before submitting.', 'error')
        elif action == 'submit':
            row.submitted = True
        else:
            flash('Progress saved. You can resume from Quizzes & tests.', 'success')
        db.session.commit()
        return redirect(url_for('quizzes.take', quiz_id=row.id))
    score = sum(row.answers.get(str(i)) == q['correct'] for i, q in enumerate(row.questions)) if row.submitted else None
    misses = [i for i, q in enumerate(row.questions) if row.answers.get(str(i)) != q['correct']] if row.submitted else []
    return render_template('quiz_attempt.html', quiz=row, score=score, misses=misses)


@quizzes.post('/quizzes/<int:quiz_id>/retry')
@login_required
def retry(quiz_id):
    row = QuizAttempt.query.filter_by(id=quiz_id, user_id=current_user.id).first_or_404()
    if not row.submitted:
        abort(400, 'Submit the set before retrying missed questions.')
    missed = [q for i, q in enumerate(row.questions) if row.answers.get(str(i)) != q['correct']]
    if not missed:
        return redirect(url_for('quizzes.builder', subject=row.subject))
    import random
    questions = []
    for q in missed:
        order = list(range(4))
        random.SystemRandom().shuffle(order)
        questions.append({**q, 'options': [q['options'][i] for i in order], 'correct': order.index(q['correct'])})
    retry = QuizAttempt(user_id=current_user.id, subject=row.subject, questions=questions, answers={})
    db.session.add(retry)
    db.session.commit()
    return redirect(url_for('quizzes.take', quiz_id=retry.id))
