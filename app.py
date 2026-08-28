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



# ==========================
# LOGIN
# ==========================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"



@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))





with app.app_context():

    db.create_all()







# ==========================
# HOME DASHBOARD
# ==========================

@app.route("/", methods=["GET","POST"])
def home():

    answer = ""

    latest_result = None

    ai_insight = None



    if current_user.is_authenticated:


        latest_result = DiagnosticResult.query.filter_by(

            user_id=current_user.id

        ).order_by(

            DiagnosticResult.id.desc()

        ).first()



        if latest_result:


            ai_insight = {

                "strengths": latest_result.strengths,

                "weaknesses": latest_result.weaknesses,

                "recommendation": latest_result.recommendation

            }







    if request.method == "POST":


        question_text = request.form["question"]



        answer = (

            "StudyAI analyzed your question. "

            "Personalized feedback generated."

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

        answer=answer,

        latest_result=latest_result,

        ai_insight=ai_insight

    )









# ==========================
# SIGNUP
# ==========================

@app.route("/signup", methods=["GET","POST"])
def signup():


    if request.method == "POST":


        username=request.form["username"]

        email=request.form["email"]

        password=request.form["password"]




        exists = User.query.filter_by(

            email=email

        ).first()



        if exists:


            flash(

                "Account already exists.",

                "error"

            )


            return redirect(

                url_for("signup")

            )




        user = User(

            username=username,

            email=email,

            password=generate_password_hash(password)

        )


        db.session.add(user)

        db.session.commit()



        return redirect(

            url_for("login")

        )




    return render_template(

        "signup.html"

    )









# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET","POST"])
def login():


    if request.method=="POST":


        email=request.form["email"]

        password=request.form["password"]



        user=User.query.filter_by(

            email=email

        ).first()




        if user is None:


            flash(

                "No account exists.",

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

                "Wrong password.",

                "error"

            )


            return redirect(

                url_for("login")

            )



        login_user(user)



        return redirect(

            url_for("home")

        )




    return render_template(

        "login.html"

    )









# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
@login_required
def logout():


    logout_user()


    return redirect(

        url_for("home")

    )









# ==========================
# PROFILE
# ==========================

@app.route("/profile")
@login_required
def profile():


    return render_template(

        "profile.html"

    )









# ==========================
# DIAGNOSTIC ENGINE
# ==========================

@app.route("/diagnostic", methods=["GET","POST"])
@login_required
def diagnostic():


    selected_subject=list(ap_topics.keys())[0]


    topics=ap_topics[selected_subject]


    report=None





    if request.method=="POST":



        selected_subject=request.form["subject"]


        topics=ap_topics[selected_subject]



        scores={}



        for topic in topics:


            scores[topic]=int(

                request.form.get(

                    topic,

                    3

                )

            )





        readiness=int(

            (

                sum(scores.values())

                /

                (len(scores)*5)

            )

            *

            100

        )





        if readiness>=85:

            predicted="5"

        elif readiness>=70:

            predicted="4"

        elif readiness>=55:

            predicted="3"

        else:

            predicted="2"







        strengths=[

            x for x,y in scores.items()

            if y>=4

        ]



        weaknesses=[

            x for x,y in scores.items()

            if y<=2

        ]





        recommendation=(

            "Study next: "

            +

            ", ".join(weaknesses)

            if weaknesses

            else

            "Continue advanced practice."

        )







        result=DiagnosticResult(

            subject=selected_subject,

            readiness=readiness,

            predicted_score=predicted,

            strengths=", ".join(strengths),

            weaknesses=", ".join(weaknesses),

            recommendation=recommendation,

            user_id=current_user.id

        )



        db.session.add(result)

        db.session.commit()





        report={

            "readiness":readiness,

            "prediction":{

                "score":predicted

            },

            "strengths":strengths,

            "weaknesses":weaknesses,

            "recommendation":recommendation

        }







    return render_template(

        "diagnostic.html",

        subjects=ap_topics.keys(),

        selected_subject=selected_subject,

        topics=topics,

        report=report

    )









# ==========================
# KNOWLEDGE GALAXY
# ==========================

@app.route("/galaxy")
@login_required
def galaxy():

    latest_result = DiagnosticResult.query.filter_by(

        user_id=current_user.id

    ).order_by(

        DiagnosticResult.id.desc()

    ).first()


    topics = []



    if latest_result:


        if latest_result.strengths:

            for topic in latest_result.strengths.split(", "):

                topics.append(topic)



        if latest_result.weaknesses:

            for topic in latest_result.weaknesses.split(", "):

                topics.append(topic)





    return render_template(

        "galaxy.html",

        topics=topics

    )

    latest_result=DiagnosticResult.query.filter_by(

        user_id=current_user.id

    ).order_by(

        DiagnosticResult.id.desc()

    ).first()



    topics=[]



    if latest_result:


        if latest_result.strengths:


            for topic in latest_result.strengths.split(", "):

                topics.append({

                    "name":topic,

                    "level":5

                })



        if latest_result.weaknesses:


            for topic in latest_result.weaknesses.split(", "):

                topics.append({

                    "name":topic,

                    "level":2

                })






    return render_template(

        "galaxy.html",

        topics=topics

    )









# ==========================
# ABOUT
# ==========================

@app.route("/about")
def about():

    return render_template(

        "about.html"

    )









if __name__=="__main__":

    app.run(debug=True)
