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
        new_question = Question(question_text = question)
        new_option1 = Option( option_text = request.form.get('c1'))
        new_option2 = Option( option_text = request.form.get('c2'))
        new_option3 = Option( option_text = request.form.get('c3'))
        new_option4 = Option( option_text = request.form.get('c4'))


        db.session.add(new_quiz)
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
