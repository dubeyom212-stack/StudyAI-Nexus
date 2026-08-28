from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()



class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )



    diagnostics = db.relationship(
        "DiagnosticResult",
        backref="user",
        lazy=True
    )





class Question(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.String(500)
    )

    answer = db.Column(
        db.String(2000)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )
class DiagnosticResult(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    subject = db.Column(
        db.String(100)
    )


    readiness = db.Column(
        db.Integer
    )


    predicted_score = db.Column(
        db.String(10)
    )


    strengths = db.Column(
        db.Text
    )


    weaknesses = db.Column(
        db.Text
    )


    recommendation = db.Column(
        db.Text
    )


    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )




