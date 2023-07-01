from flask import Blueprint,render_template,request, flash, redirect,url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Quiz, Question, Option

views = Blueprint('views', __name__)
auth = Blueprint('auth', __name__)

@views.route('/' , methods = ['GET' , 'POST'])
@login_required
def home(): 
    if request.method == 'POST':
        usr_search = request.form.get('search_usr')
        usr_query =  User.query.filter(User.first_name.like(usr_search)).all()
        return render_template("home.html", user = current_user, usr_search_results = usr_search)
    return render_template("home.html", user = current_user)



@views.route('/quizmaker' , methods = ['GET' , 'POST'])
@login_required
def quizmaker():
    if request.method == 'POST':
        data = request.get_json()
        quiz_name = data.get('quiz_name')
        quiz_desc = data.get('quiz_desc')
        new_quiz = Quiz(user_id = current_user.id, quiz_title = quiz_name, quiz_description = quiz_desc)
        db.session.add(new_quiz)
        db.session.commit()

        for x in range (1, 10):
            question = data.get(f'question{x}')
            if question == None:
                break
            quiz_id = new_quiz.quiz_id
            new_question = Question(quiz_id = quiz_id,question_text = question)
            db.session.add(new_question)
            db.session.commit()

            question_id = new_question.question_id
            new_option = []
            new_option.append(Option( question_id = question_id,option_text = data.get(f'q{x}_c1'), is_correct = True))
            new_option.append(Option(question_id = question_id, option_text = data.get(f'q{x}_c2'),is_correct = False))
            new_option.append(Option( question_id = question_id,option_text = data.get(f'q{x}_c3'), is_correct = False))
            new_option.append(Option( question_id = question_id,option_text = data.get(f'q{x}_c4'), is_correct = False))
            db.session.add(new_option[0])
            db.session.add(new_option[1])
            db.session.add(new_option[2])
            db.session.add(new_option[3])
            db.session.commit()
        return redirect(url_for('views.home'))

    return render_template("quizmaker.html", user = current_user)


@views.route('/profile/<profile>')
@login_required
def show_profile(profile):
    user_query = User.query.filter(User.first_name == profile).first()
    quiz_query = Quiz.query.filter(Quiz.user_id == user_query.id).all()
    return render_template('profile.html', user = user_query, quizes = quiz_query)

@views.route('/profile/my_profile')
@login_required
def show_user_profile():
    quiz_query = Quiz.query.filter(Quiz.user_id == current_user.id).all()
    return render_template('profile.html', user = current_user, quizes = quiz_query)

@views.route('/quiz_taker/<quizz_id>')
@login_required
def take_quiz(quizz_id):
    quiz_query = Quiz.query.filter(Quiz.quiz_id == quizz_id).first()
    question_query = Question.query.filter(Question.quiz_id == quizz_id).all()

    return render_template("quiz_taker.html",user = current_user, query1= quiz_query, query2 = question_query)



# Debugging purpose
@views.route('/test')
def test():
    query1 = User.query.all()
    query2 = Quiz.query.all()
    query3 = Question.query.all()
    query4 = Option.query.all() 
    return render_template('test.html', message1 = query1 , message2 = query2,message3 = query3,message4 = query4, user = current_user)

@views.route('/delete')
def delete():
    query= Quiz.query.delete()
    db.session.commit()
    query= Question.query.delete()
    db.session.commit()
    query= Option.query.delete()
    db.session.commit()

    return redirect(url_for('views.home'))