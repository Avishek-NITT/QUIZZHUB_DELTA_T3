from flask import Blueprint,render_template,request, flash, redirect,url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Quiz, Question, Option, Score, User_profile, User_Friends
from werkzeug.utils import secure_filename
import random
import base64


views = Blueprint('views', __name__)
auth = Blueprint('auth', __name__)

@views.route('/' , methods = ['GET' , 'POST'])
@login_required
def home(): 
    if request.method == 'POST':
        usr_search = request.form.get('search_usr')
        usr_query =  User.query.filter(User.first_name.like(usr_search)).all()
        return render_template("home.html", user = current_user, usr_search_results = usr_query)
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
    current_user_query = User.query.filter(User.id == current_user.id).first()
    user_query = User.query.filter(User.first_name == profile).first()
    profile_img_query = ""
    query = User_profile.query.filter(User_profile.user_id == user_query.id).first()
    if query:
        profile_img_query = base64.b64encode(query.profile_img).decode('utf-8')
    if not user_query:
        return render_template('home.html', user = current_user)
    if user_query.first_name == current_user.first_name:
        return redirect(url_for('views.show_user_profile'))
    quiz_query = Quiz.query.filter(Quiz.user_id == user_query.id).all()
    quiz_taken_query1 = Score.query.filter(Score.user_id == user_query.id).all()
    user_frnd_query = ""
    user_frnd_query = User_Friends.query.filter(User_Friends.sender_user == current_user_query.first_name,
                                                User_Friends.recieved_user == user_query.first_name).all()
    if quiz_taken_query1:
        quiz_taken_query2 =[]
        for x in quiz_taken_query1:
            quiz_taken_query2.append(Quiz.query.filter(Quiz.quiz_id == x.quiz_id).all())
        return render_template('profile.html', user= current_user_query,profile_user = user_query, quizes = quiz_query, 
                            quiz_taken1 = quiz_taken_query1, quiz_taken2 = quiz_taken_query2, 
                            prof_img = profile_img_query, frnd_query = user_frnd_query)
    else:
        return render_template('profile.html', user= current_user_query, profile_user = user_query, quizes = quiz_query, 
                                                prof_img = profile_img_query,frnd_query = user_frnd_query)

@views.route('/profile/my_profile', methods = ['GET', 'POST'])
@login_required
def show_user_profile():
    if request.method == 'POST':
        if not request.files['profile_pic']:
            return redirect(url_for('views.home'))
        
        #delete user's previous image
        profile_pic = request.files['profile_pic']
        db.session.query(User_profile).filter(User_profile.user_id == current_user.id).delete()
        img = User_profile(user_id = current_user.id, profile_img = profile_pic.read())
        db.session.add(img)
        db.session.commit()
    profile_img_query = ""
    query = User_profile.query.filter(User_profile.user_id == current_user.id).first()
    if query:
        profile_img_query = base64.b64encode(query.profile_img).decode('utf-8')
    quiz_query = Quiz.query.filter(Quiz.user_id == current_user.id).all()
    quiz_taken_query1 = Score.query.filter(Score.user_id == current_user.id).all()
    if quiz_taken_query1:
        quiz_taken_query2 =[]
        for x in quiz_taken_query1:
            quiz_taken_query2.append(Quiz.query.filter(Quiz.quiz_id == x.quiz_id).all())
        return render_template('user_profile.html', user = current_user, quizes = quiz_query, quiz_taken1 = quiz_taken_query1, quiz_taken2 = quiz_taken_query2, prof_img = profile_img_query)
    else:
        return render_template('user_profile.html', user = current_user, quizes = quiz_query, prof_img = profile_img_query)

@views.route('/quiz_taker/<quizz_id>', methods = ['GET' , 'POST'])
@login_required
def take_quiz(quizz_id):
    quiz_query = Quiz.query.filter(Quiz.quiz_id == quizz_id).first()
    question_query = Question.query.filter(Question.quiz_id == quizz_id).all()
    option_query = []
    score = 0
    for x in question_query:
        option  = Option.query.filter(Option.question_id == x.question_id).all()
        random.shuffle(option)
        option_query.append(option)
    if request.method == 'POST':
        data = request.get_json()
        question_id  = Question.query.filter(Question.quiz_id == quizz_id).all()
        
        for x in range(1,len(question_id) + 1):
            chosen_option = data.get(f"{x}")
            
            option = Option.query.filter(Option.question_id == question_id[x-1].question_id, Option.option_text == chosen_option).first()
            if(option.is_correct == True):
                score = score + 1
        new_score = Score(quiz_id = quizz_id, user_id = current_user.id, user_score = score)
        db.session.add(new_score)
        db.session.commit()
        return render_template("quiz_taker.html",user = current_user, quiz_query= quiz_query, question_query = question_query,option_query = option_query, user_score = score)
    else:
        return render_template("quiz_taker.html",user = current_user, quiz_query= quiz_query, question_query = question_query,option_query = option_query)



# Debugging purpose
@views.route('/test')
def test():
    query1 = User.query.all()
    query2 = Quiz.query.all()
    query3 = Question.query.all()
    query4 = Option.query.all() 
    query5 = Score.query.all()
    query6 = User_profile.query.all()
    query7 = User_Friends.query.all()
    return render_template('test.html', message1 = query1 , message2 = query2,message3 = query3,message4 = query4, message5 = query5 ,message6 = query6,message7= query7, user = current_user)

@views.route('/delete')
def delete():
    # query = User.query.delete()
    # db.session.commit()
    # query= Quiz.query.delete()
    # db.session.commit()
    # query= Question.query.delete()
    # db.session.commit()
    # query= Option.query.delete()
    # db.session.commit()
    # query = Score.query.delete()
    # db.session.commit()
    # query = User_profile.query.delete()
    # db.session.commit()
    # query = User_Friends.query.delete()
    # db.session.commit()
    query = User_Friends(sender_user = "Avishek", recieved_user = "Avyyukt", frnd_status = 0)
    db.session.add(query)
    db.session.commit()

    return redirect(url_for('views.home'))