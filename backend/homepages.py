from flask import Blueprint, render_template, session, redirect, url_for

homepages_bp = Blueprint('homepages', __name__)


def login_required(role=None):
    def wrapper(func):
        def decorated_view(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('auth.login'))

            if role == 'user' and session.get('role') == 'admin':
                return redirect(url_for('homepages.admin_home'))

            if role == 'admin' and session.get('role') == 'user':
                return redirect(url_for('homepages.user_home'))

            return func(*args, **kwargs)

        decorated_view.__name__ = func.__name__
        return decorated_view

    return wrapper


@homepages_bp.route('/admin')
@login_required(role='admin')
def admin_home():
    return render_template('admin_home.html')

@homepages_bp.route('/user')
@login_required(role='user')
def user_home():
    return render_template('user_home.html')


@homepages_bp.route('/catalog')
def catalog():
    return render_template('catalog.html')