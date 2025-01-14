from app import MyApp, MyDb
from app.forms import LoginForm, RegisterForm
from app.models import Utilisateur
from flask import flash, redirect, render_template, url_for, request, Response
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.openAI import g_messages, generate_response, reset_messages

@MyApp.route('/')
@MyApp.route('/index')
def index():
    print(MyApp.config["SQLALCHEMY_DATABASE_URI"])
    return render_template('index.html')

@MyApp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = MyDb.session.scalar(sa.select(Utilisateur).where(Utilisateur.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Identifiant ou mot de passe incorrect', category="error")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form = form)

@MyApp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = Utilisateur(prenom=form.prenom.data, email=form.email.data)
        user.set_password(form.password.data)
        MyDb.session.add(user)
        MyDb.session.commit()
        flash('Félicitations ! Vous êtes bien enregistré')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
 
@MyApp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@MyApp.route('/users')
@login_required
def users():
    users = MyDb.session.execute(MyDb.select(Utilisateur)).scalars()
    return render_template('users.html', users=users)

@MyApp.route('/message/<version>', methods = ['POST'])
@login_required
def message(version):
    user_input = request.get_json()
    message = user_input['message']

    # Save to DB, call NLP, etc
    g_messages.append({"role": "user", "content": message })
    print(f"{message=}")
  
    return {'message': message}

@MyApp.route('/bot/<version>')
@login_required
def bot(version):
    return Response(generate_response(MyApp, version), mimetype='text/event-stream')

@MyApp.route('/chat_35', methods=['GET', 'POST'])
@login_required
def chat_35():
    g_messages = reset_messages()
    return render_template('chat_35.html')

@MyApp.route('/chat_4', methods=['GET', 'POST'])
@login_required
def chat_4():
    g_messages = reset_messages()
    return render_template('chat_4.html')
