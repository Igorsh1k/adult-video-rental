from flask import Blueprint, request, jsonify
from database import add_movie, get_movie, update_movie, delete_movie, list_movies
import database

video_bp = Blueprint('video', __name__)

@video_bp.route('/movies', methods=['GET'])
def get_movies():
    movies = list_movies()
    return jsonify(movies)

@video_bp.route('/movies/<movie_id>', methods=['GET'])
def get_single_movie(movie_id):
    movie = get_movie(movie_id)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

@video_bp.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    add_movie(
        title=data['title'],
        description=data['description'],
        is_adult=data['is_adult'],
        is_available=data.get('is_available', True),
        owner=data.get('owner', 'store')
    )
    return jsonify({"message": "Movie added successfully"}), 201

@video_bp.route('/movies/<movie_id>', methods=['PUT'])
def update_movie_details(movie_id):
    data = request.get_json()
    update_movie(movie_id, data)
    return jsonify({"message": "Movie updated successfully"}), 200

@video_bp.route('/movies/<movie_id>', methods=['DELETE'])
def delete_single_movie(movie_id):
    delete_movie(movie_id)
    return jsonify({"message": "Movie deleted successfully"}), 200
