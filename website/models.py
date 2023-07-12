from . import db 
from flask_login import UserMixin




class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quiz_title = db.Column(db.String)
    quiz_description = db.Column(db.String)
    user = db.relationship("User")

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'))
    question_text = db.Column(db.String)
    quiz = db.relationship("Quiz")

class Option(db.Model):
    __tablename__ = 'options'
    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    option_text = db.Column(db.String)
    is_correct = db.Column(db.Boolean)
    question = db.relationship("Question")


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    user_score = db.Column(db.Integer)


class User_profile(db.Model):
    __tablename__ = 'user_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    profile_img = db.Column(db.LargeBinary, default=None)
    user = db.relationship('User', backref='profile', uselist=False)