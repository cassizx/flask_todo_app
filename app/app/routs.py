from flask import Flask, request, render_template, redirect, url_for, g, abort
from flask.helpers import url_for
from app import app, api
from .apis import AllTasksView, Todo
from .auth import sign_up as sign_up_, login as login_, reset_password, reset_with_token_, confurm_email_with_token
from flask_login import logout_user, login_required, current_user


@app.route('/singup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('singup.html')

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    return sign_up_(name, email, str(password))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        if email is not None and password is not None:
            return login_(email, str(password))

    if current_user.is_authenticated:
        return redirect('/')

    return render_template('login.html')


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        return render_template('reset.html')

    if request.method == 'POST' and request.form.get('email') != '':
        return reset_password(request.form.get('email'))
    else:
        return render_template('404.html'), 404


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):

    if request.method == 'GET':
        return render_template('reset_with_token.html', token=token)

    try:
        return reset_with_token_(token)
    except:
        abort(404)


@app.route('/confurm/<token>', methods=["GET", "POST"])
def confurm_email(token):
    # if request.method == 'GET':
    #     return render_template('reset_with_token.html', token=token)
    try:
        return confurm_email_with_token(token)
    except:
        abort(404)


@app.route('/', methods=['GET'])
@login_required
def index():
    if current_user.is_authenticated:
	    return render_template('index.html', name=current_user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


api.add_resource(AllTasksView, '/api/tasks', '/api/tasks/')
api.add_resource(Todo, '/api/task/<int:todo_id>/', '/api/task/add', '/api/task/add/')
