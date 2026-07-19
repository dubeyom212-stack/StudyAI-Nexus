from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from ap_data import ap_topics
from study_plan import create_plan

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studyai.db"

db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    answer = db.Column(db.String(2000))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    goal = db.Column(db.String(100))


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        question_text = request.form["question"]

        answer = "This is where the AI answer will appear."

        new_question = Question(
            question=question_text,
            answer=answer
        )

        db.session.add(new_question)
        db.session.commit()


    history = Question.query.all()

    return render_template(
        "index.html",
        answer=answer,
        history=history
    )


@app.route("/diagnostic", methods=["GET", "POST"])
def diagnostic():

    weaknesses = []
    plan = []

    selected_subject = request.form.get(
        "subject",
        "AP Calculus BC"
    )


    if request.method == "POST":

        if "analyze" in request.form:

            for topic in ap_topics[selected_subject]:

                score = request.form.get(topic)

                if score and int(score) <= 2:
                    weaknesses.append(topic)

            plan = create_plan(weaknesses)


    return render_template(
        "diagnostic.html",
        subjects=ap_topics.keys(),
        topics=ap_topics[selected_subject],
        selected_subject=selected_subject,
        weaknesses=weaknesses,
        plan=plan
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():

    if request.method == "POST":

        name = request.form["name"]
        grade = request.form["grade"]
        goal = request.form["goal"]

        student = Student(
            name=name,
            grade=grade,
            goal=goal
        )

        db.session.add(student)
        db.session.commit()


    students = Student.query.all()

    return render_template(
        "profile.html",
        students=students
    )


if __name__ == "__main__":
    app.run(debug=True)
    