import functools
from . import login_manager
from flask_login import current_user, login_user, logout_user

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, make_response, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

# from ClassSpace.db import get_db
from .data.models.user import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Convert form data to JSON
    req_data = request.get_json()

    # Null check email and password of form
    if request.method == 'POST':
        email = req_data['email']
        password = req_data['password']
        error = None

        if not email:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # If both are present, check to make sure this email has not already been registered
        else:
            user = User.query.filter(User.email == email).first()
            error = f'User {user.email} is already registered.' if user else None

        # If the above checks pass, insert newly created user in `users` table
        if not error:
            user_to_add = User(email=email,
                               password=generate_password_hash(password),
                               first_name='Alex',
                               last_name='Perez',
                               school_name='Northeastern University')
            db.session.add(user_to_add)
            db.session.commit()
            # return redirect(url_for('auth.login'))
            return make_response(f"New user created successfully")

        flash(error)

    # If request was a GET, send them to the login page
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return jsonify(status='ok')

    # Convert form data to JSON
    req_data = request.get_json()

    # Pull values from JSON
    email = req_data['email']
    password = req_data['password']
    user = None

    if not email or not password:
        error = 'Email and Password are required.'
        return make_response(error, 401)

    # try to query for the user
    user = User.query.filter(User.email == email).first()

    # If they don't exist, throw error
    if not user:
        error = 'No user exists with this email address'
        return make_response(error, 401)

    # If passwords don't match, throw error
    elif not check_password_hash(user.password, password):
        error = 'Incorrect Password'
        return make_response(error, 401)

    # If they're here, then everything worked and we can log the user in
    login_user(user)
    #session.clear()
    #session['user_id'] = user.id
    return redirect(url_for('dashboard'))


@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if session.get('user_id') is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view

# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')
#     if not user_id:
#         g.user = None
#     else:
#         g.user = User.query.filter(User.id == user_id).first()

@login_manager.user_loader
def load_user(id):
    result = User.query.filter(User.id == id).first()
    return result
