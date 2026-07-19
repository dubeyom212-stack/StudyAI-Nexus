from flask import Flask, render_template, request, redirect, url_for, flash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db, User, Question, DiagnosticResult

from ap_data import ap_topics





app = Flask(__name__)


app.config["SECRET_KEY"] = "studyai-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studyai.db"



db.init_app(app)





# -------------------------
# LOGIN SYSTEM
# -------------------------

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"




@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))





with app.app_context():

    db.create_all()







# -------------------------
# HOME DASHBOARD
# -------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""


    if request.method == "POST":


        question_text = request.form["question"]



        answer = (

            "StudyAI is analyzing your question. "

            "Your personalized AI explanation will appear here."

        )



        if current_user.is_authenticated:


            question = Question(

                question=question_text,

                answer=answer,

                user_id=current_user.id

            )


            db.session.add(question)

            db.session.commit()





    return render_template(

        "index.html",

        answer=answer

    )









# -------------------------
# SIGNUP
# -------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():


    if request.method == "POST":


        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]





        existing_user = User.query.filter_by(

            email=email

        ).first()



        if existing_user:


            flash(

                "An account with this email already exists.",

                "error"

            )


            return redirect(

                url_for("signup")

            )






        hashed_password = generate_password_hash(

            password

        )



        user = User(

            username=username,

            email=email,

            password=hashed_password

        )



        db.session.add(user)

        db.session.commit()





        flash(

            "Account created successfully! Please login.",

            "success"

        )



        return redirect(

            url_for("login")

        )






    return render_template(

        "signup.html"

    )









# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():


    if request.method == "POST":



        email = request.form["email"]

        password = request.form["password"]





        user = User.query.filter_by(

            email=email

        ).first()





        if user is None:


            flash(

                "No account exists with this email.",

                "error"

            )


            return redirect(

                url_for("login")

            )






        if not check_password_hash(

            user.password,

            password

        ):



            flash(

                "Incorrect password.",

                "error"

            )


            return redirect(

                url_for("login")

            )






        login_user(user)





        flash(

            "Welcome back!",

            "success"

        )



        return redirect(

            url_for("profile")

        )







    return render_template(

        "login.html"

    )









# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
@login_required
def logout():


    logout_user()



    return redirect(

        url_for("home")

    )









# -------------------------
# PROFILE
# -------------------------

@app.route("/profile")
@login_required
def profile():


    return render_template(

        "profile.html"

    )









# -------------------------
# DIAGNOSTIC ENGINE
# -------------------------

@app.route("/diagnostic", methods=["GET", "POST"])
@login_required
def diagnostic():


    selected_subject = list(

        ap_topics.keys()

    )[0]



    topics = ap_topics[selected_subject]



    report = None






    if request.method == "POST":



        selected_subject = request.form.get(

            "subject"

        )



        topics = ap_topics[selected_subject]






        if "analyze" in request.form:




            scores = {}




            for topic in topics:



                scores[topic] = int(

                    request.form.get(

                        topic,

                        3

                    )

                )







            readiness = int(

                (

                    sum(scores.values())

                    /

                    (len(scores) * 5)

                )

                *

                100

            )







            strengths = [

                topic

                for topic, score in scores.items()

                if score >= 4

            ]





            weaknesses = [

                topic

                for topic, score in scores.items()

                if score <= 2

            ]







            if readiness >= 85:


                predicted_score = "5"



            elif readiness >= 70:


                predicted_score = "4"



            elif readiness >= 55:


                predicted_score = "3"



            else:


                predicted_score = "2"








            result = DiagnosticResult(


                subject=selected_subject,


                readiness=readiness,


                predicted_score=predicted_score,


                user_id=current_user.id


            )




            db.session.add(result)

            db.session.commit()







            report = {


                "readiness": readiness,



                "prediction": {


                    "score": predicted_score,


                    "confidence": "Estimated",


                    "explanation":
                    "Generated from your AP mastery ratings."

                },



                "profile":

                "Your learning profile is based on your mastery strengths and weaknesses.",



                "strengths": strengths,



                "weaknesses": weaknesses,



                "root_causes": [],



                "recommendation":

                "Review weak concepts first, then practice AP-style questions."

            }







    return render_template(

        "diagnostic.html",


        subjects=ap_topics.keys(),


        selected_subject=selected_subject,


        topics=topics,


        report=report

    )









# -------------------------
# ABOUT
# -------------------------

@app.route("/about")
def about():


    return render_template(

        "about.html"

    )









if __name__ == "__main__":


    app.run(debug=True)
    