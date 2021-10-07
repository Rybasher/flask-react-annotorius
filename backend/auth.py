from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    req = request.get_json(force=True)
    username, password = req.get('username', None), req.get('password', None)
    user = User.query.filter_by(username=username).first()
    remember = True if req.get('remember') else False
    if not user or not check_password_hash(user.password, password):
        return {"status": "bad", "result": "Enter valid data"}
    login_user(user, remember=remember)
    return {"status": "ok", "message": "Welcome"}


@auth.route('/api/sign-up', methods=['POST', 'GET'])
def signup():
    req = request.get_json(force=True)
    username, password, project_name = req.get('username', None), req.get('password', None), req.get('project', None)
    user = User.query.filter_by(username=username).first()
    if user:
        return {"status": "bad", "result": "User is not created"}
    db.session.add(User(
        username=username,
        password=generate_password_hash(password),
        roles='admin',
        project_name=project_name
    ))
    db.session.commit()
    return {"status": "ok", "result": "User created"}, 200


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return {"status": "ok", "result": "Goodbye"}
