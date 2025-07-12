from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegisterForm, AskQuestionForm
from models import db, User
from models import Question, db, Answer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stackit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    return render_template('home.html', questions=questions)

@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask_question():
    form = AskQuestionForm()
    if form.validate_on_submit():
        question = Question(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(question)
        db.session.commit()
        flash('Your question has been posted!', 'success')
        return redirect(url_for('home'))
    return render_template('ask.html', form=form)

@app.route('/question/<int:question_id>')
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question.id).all()
    return render_template('answer.html', question=question, answers=answers)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
