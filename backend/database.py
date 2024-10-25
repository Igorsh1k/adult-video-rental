from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['adult-video-rental-DB']
users_collection = db['users']

def init_db():
    if 'users' not in db.list_collection_names():
        db.create_collection('users')

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
