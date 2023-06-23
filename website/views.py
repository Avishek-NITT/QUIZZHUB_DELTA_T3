from flask import Blueprint,render_template,request, flash
from flask_login import login_required, current_user
from . import db
from .models import User, Quiz, Question, Option

views = Blueprint('views', __name__)

@views.route('/' , methods = ['GET' , 'POST'])
@login_required
def home(): 
    return render_template("home.html", user = current_user)



@views.route('/quizmaker' , methods = ['GET' , 'POST'])
@login_required
def quizmaker():
    if request.method == 'POST':
        quiz_name = request.form.get('quiz_name')
        quiz_desc= request.form.get('quiz_desc')
        question = request.form.get('question1')


        new_quiz = Quiz(user_id = current_user.id, quiz_title = quiz_name, quiz_description = quiz_desc)
        db.session.add(new_quiz)
        db.session.commit()
        
        quiz_id = new_quiz.quiz_id
        new_question = Question(quiz_id = quiz_id,question_text = question)
        db.session.add(new_question)
        db.session.commit()
        
        question_id = new_question.question_id
        new_option1 = Option( question_id = question_id,option_text = request.form.get('c1'), is_correct = True)
        new_option2 = Option(question_id = question_id, option_text = request.form.get('c2'),is_correct = False)
        new_option3 = Option( question_id = question_id,option_text = request.form.get('c3'), is_correct = False)
        new_option4 = Option( question_id = question_id,option_text = request.form.get('c4'), is_correct = False)



        db.session.add(new_question)
        db.session.add(new_option1)
        db.session.add(new_option2)
        db.session.add(new_option3)
        db.session.add(new_option4)
        db.session.commit()

    return render_template("quizmaker.html", user = current_user)


@views.route('/profile')
@login_required
def show_profile():
    query = Quiz.query.filter(Quiz.user_id == current_user.id).all()
    return render_template('profile.html', user = current_user, quizes = query)


@views.route('/quiz_taker/<quiz_id>')
@login_required
def take_quiz(quiz_id):
    quiz_query = Quiz.query.filter(Quiz.quiz_id == quiz_id).all()
    question_query = Question.query.filter(Question.quiz_id == quiz_id).all()
    return f"<h1> {question_query}</h1>"
    for x in question_query:
        return "<h1> Here </h1>"
        option_query = Option.query.filter(Option.question_id == x.question_id).all()
    return render_template("quiz_taker.html", quiz = quiz_query, question = question_query, option= option_query)