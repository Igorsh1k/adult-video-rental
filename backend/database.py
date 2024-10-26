from pymongo import MongoClient

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
def add_movie(title, description, is_adult, is_available=True, owner="store"):
    movie_data = {
        'title': title,
        'description': description,
        'is_adult': is_adult,
        'is_available': is_available,
        'owner': owner
    }
    movies_collection.insert_one(movie_data)

def get_movie(movie_id):
    return movies_collection.find_one({'_id': movie_id})

def update_movie(movie_id, update_data):
    movies_collection.update_one({'_id': movie_id}, {'$set': update_data})

def delete_movie(movie_id):
    movies_collection.delete_one({'_id': movie_id})

def list_movies():
    return list(movies_collection.find())