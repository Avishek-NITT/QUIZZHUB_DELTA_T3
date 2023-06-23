from flask import Blueprint,render_template,request, flash
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/' , methods = ['GET' , 'POST'])
@login_required
def home():
    # if request.method == 'POST':
    #     quiz_name = request.form.get('quiz_name')
    #     quiz_question = request.form.get('question1')
    #     quiz_id = Quiz_collection.query.filter( Quiz_collection.Quiz_name == quiz_name)
        
    #     new_quiz = Quiz_collection(Quiz_Id = current_user.id, Quiz_name = quiz_name)
    #     new_question = Quiz_Questions(Quiz_Id = quiz_id , Quiz_Question = quiz_question)


    #     db.session.add(new_quiz)
    #     db.session.add(new_question)
    #     db.session.commit()


    return render_template("home.html", user = current_user)