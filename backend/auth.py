from flask import Blueprint, request, redirect, render_template, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_user, add_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('homepages.admin_home'))
            else:
                return redirect(url_for('homepages.user_home'))
        return "Invalid credentials"
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        birthdate = request.form['birthdate']
        role = 'user'
        add_user(username, generate_password_hash(password), role, birthdate)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))


def list_user_movies(username):
    user_movies = movies_collection.find({"owner": username})
    return [format_movie(movie) for movie in user_movies]


