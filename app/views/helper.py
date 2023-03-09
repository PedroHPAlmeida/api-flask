import datetime

import jwt
from . import users
from app import app
from werkzeug.security import check_password_hash
from flask import request, jsonify
from functools import wraps


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = users.get_user_by_username(auth.username)
    if not user:
        return jsonify({'message': 'user not found', 'data': {}}), 401

    if user and check_password_hash(user.password, auth.password):
        exp = datetime.datetime.now() + datetime.timedelta(hours=12)
        token = jwt.encode({'username': auth.username, 'exp': exp},
                           app.config['SECRET_KEY'])
        return jsonify({'message': 'validated successfully', 'token': token,
                       'exp': exp})
    return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'token is missing', 'data': []}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], ['HS256'])
            current_user = users.get_user_by_username(username=data['username'])
        except:
            return jsonify({'message': 'token is invalid or expired', 'data': []}), 401
        return f(current_user, *args, **kwargs)
    return decorated
