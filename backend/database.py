from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['adult-video-rental-DB']
users_collection = db['users']
movies_collection = db['movies']

def init_db():
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
    if 'movies' not in db.list_collection_names():
        db.create_collection('movies')

def add_user(username, password, role, birthdate):
    user_data = {
        'username': username,
        'password': password,
        'role': role,
        'birthdate': birthdate
    }
    users_collection.insert_one(user_data)

def get_user(username):
    return users_collection.find_one({'username': username})



# CRUD з фільмами
def format_movie(movie):
    movie['id'] = str(movie['_id'])
    del movie['_id']
    return movie

def add_movie(title, description, is_adult, is_available=True, owner="store"):
    movie = {
        "title": title,
        "description": description,
        "is_adult": is_adult,
        "is_available": is_available,
        "owner": owner
    }
    movies_collection.insert_one(movie)

def get_movie(movie_id):
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
    if movie:
        return format_movie(movie)
    return None

def update_movie(movie_id, data):
    update_data = {k: v for k, v in data.items() if v is not None}
    movies_collection.update_one({"_id": ObjectId(movie_id)}, {"$set": update_data})

def delete_movie(movie_id):
    movies_collection.delete_one({"_id": ObjectId(movie_id)})

def list_movies():
    movies = movies_collection.find()
    return [format_movie(movie) for movie in movies]


def list_user_movies(username):
    user_movies = movies_collection.find({"owner": username})
    return [format_movie(movie) for movie in user_movies]


