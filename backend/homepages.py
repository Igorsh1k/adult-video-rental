from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from database import *
import database

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
    movies = list_movies()
    return render_template('admin_home.html', movies=movies)

@homepages_bp.route('/user')
@login_required(role='user')
def user_home():
    username = session.get('username')
    user_movies = list_user_movies(username)
    return render_template('user_home.html', user_movies=user_movies)


@homepages_bp.route('/catalog')
def catalog():
    movies = list_movies()
    return render_template('catalog.html', movies=movies)


@homepages_bp.route('/take_movie/<movie_id>', methods=['POST'])
def take_movie(movie_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    user = database.get_user(session['username'])

    if 'birth_date' not in user:
        return jsonify({"error": "Birthdate not found"}), 400

    movie = get_movie(movie_id)

    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    # Перевірка віку користувача для доступу до дорослих фільмів
    try:
        birth_date = datetime.strptime(user['birth_date'], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    age = (datetime.now() - birth_date).days // 365

    if movie['is_adult'] and age < 21:
        return jsonify({"error": "You must be 21 or older to rent this movie"}), 403

    # Перевірка доступності фільму
    if movie['owner'] == 'store' and movie['is_available']:
        update_movie(movie_id, {'owner': session['username'], 'is_available': False})
        return jsonify({"message": "Movie rented successfully"})
    else:
        return jsonify({"error": "Movie is not available"}), 400


@homepages_bp.route('/return_movie/<movie_id>', methods=['POST'])
@login_required(role='user')
def return_movie(movie_id):
    movie = get_movie(movie_id)
    if movie and movie['owner'] == session.get('username'):
        update_movie(movie_id, {'owner': 'store', 'is_available': True})
        return jsonify({"message": "Movie returned successfully"})
    return jsonify({"error": "Unable to return the movie"}), 400


@homepages_bp.route('/edit_movie/<movie_id>', methods=['GET', 'POST'])
@login_required(role='admin')
def edit_movie(movie_id):
    movie = get_movie(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        is_adult = 'is_adult' in request.form
        is_available = 'is_available' in request.form

        update_movie(movie_id, {
            'title': title,
            'description': description,
            'is_adult': is_adult,
            'is_available': is_available
        })

        return redirect(url_for('homepages.admin_home'))

    return render_template('edit_movie.html', movie=movie)


@homepages_bp.route('/delete_movie/<movie_id>', methods=['POST'])
@login_required(role='admin')
def delete_movie(movie_id):
    database.delete_movie(movie_id)
    return redirect(url_for('homepages.admin_home'))


@homepages_bp.route('/create_movie', methods=['POST'])
@login_required(role='admin')
def create_movie():
    title = request.form.get('title')
    description = request.form.get('description')
    age_category = request.form.get('age_category')

    is_adult = age_category == 'adult'

    add_movie(title, description, is_adult)

    return redirect(url_for('homepages.admin_home'))