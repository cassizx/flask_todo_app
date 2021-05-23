from flask import redirect, url_for, flash, g, abort
from flask.globals import request
from flask.templating import render_template
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from .models import User
from .utils import ts, send_email


salt = 'r9se$t7pa5ss-k2ey#1'


def sign_up(name, email, password):
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email уже используется')
        return redirect(url_for('login'))

    if email != '' and name != '' and password != '':
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        token = ts.dumps(email, salt=salt)
        subject = "Подтверждение регистрации"
        confurm_email_url = url_for(
            'confurm_email',
            token=token,
            _external=True)
        html = render_template(
            'email/confurm_email.html',
            confurm_email_url=confurm_email_url)
        send_email(email, subject, html)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешна, на Ваш email отправлено письмо с подтверждением, пожалуйста, перейдите по ссылке в письме.')
        return redirect(url_for('login'))


def login(email, password):

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Ошибка, пожалуйста, проверьте логин и пароль.')
        return redirect(url_for('login'))
    else:
        login_user(user)
        return redirect(url_for('index'))


def reset_password(email):
    print(f'{email} request for reset')
    user = User.query.filter_by(email=email).first()
    #     if not request.json or not 'firstName' or not 'lastName' in request.json:

    if user:
        subject = "Запрос сброса пароля"
        token = ts.dumps(email, salt=salt)
        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        send_email(user.email, subject, html)
        print(recover_url)
        flash('Письмо для сброса пароля отправлено')
        return redirect(url_for('login'))
    else:
        flash(f'Пользователь с email {email} не найден. Проверьте корректность email.')
        return render_template('reset.html')


def reset_with_token_(token):

    email = ts.loads(token, salt=salt, max_age=86400)

    user = User.query.filter_by(email=email).first_or_404()
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password1 == password2:
        user.password = generate_password_hash(password1, method='sha256')
        db.session.add(user)
        db.session.commit()
        flash('Пароль успешно изменён.')
        return redirect(url_for('login'))

    return redirect(url_for('signin'))


def confurm_email_with_token(token):
    try:
        email = ts.loads(token, salt=salt, max_age=604800)
        user = User.query.filter_by(email=email).first_or_404()
        user.email_is_confurmed = True
        db.session.add(user)
        db.session.commit()
        flash('Email успешно подтверждён.')
        return redirect(url_for('login'))
    except:
        abort(404)