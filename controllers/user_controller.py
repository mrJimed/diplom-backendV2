from flask import Blueprint, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from db_models.user import User

user_controller = Blueprint('user_controller', __name__, url_prefix='/user')


@user_controller.post('/registration')
def registration():
    data = request.get_json()
    if User.query.filter(User.email == str(data['email'])).first() != None:
        return 'Пользователь с таким email уже был зарегистрирован', 409
    new_user = User(
        username=str(data['username']),
        email=str(data['email']),
        password=generate_password_hash(str(data['password']))
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return {
        'username': new_user.username
    }


@user_controller.post('/authorization')
def authorization():
    data = request.get_json()
    user = User.query.filter(User.email == str(data['email'])).first()
    if user is None:
        return 'Пользователя с таким email не существует', 400
    elif not check_password_hash(user.password, str(data['password'])):
        return 'Неправильный email или пароль', 400
    login_user(user)
    return {
        'username': user.username
    }


@user_controller.post('/logout')
@login_required
def logout():
    logout_user()
    return '', 200
