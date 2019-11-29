import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ClassSpace.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Null check email and password of form
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # If both are present, check to make sure this email has not already been registered
        elif db.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone():
            error = f'User {email} is already registered.'

        elif not db.execute(
            'SELECT * FROM domains WHERE site = ?', (email.split('@')[0], )
        ).fetchone():
            error = 'Must be a valid NEU email address'

        # If the above checks pass, insert newly created user in `users` table
        if not error:
            db.execute(
                'INSERT INTO users (email, password) VALUES (?, ?)',
                (email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    # If request was a GET, send them to the login page
    return redirect(url_for('login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = None

        if not email:
            error = 'Email is required.'

        elif not password:
            error = 'password is required.'

        if not error:
            user = db.execute(
                'SELECT * from users WHERE email = ?', (email,)
            ).fetchone()

        if not user:
            error = 'Incorrect Email'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Password'

        if not error:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))

        flash(error)

    return url_for('auth.login')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if not user_id:
        g.user = None

    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?' (user_id,)
        ).fetchone()


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('dashboard'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
