import json
from pymongo import MongoClient

def save_movies_json(movies, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(movies, file, ensure_ascii=False, indent=4)
    print(f"Movies saved to {filename}")

def save_movies_mongo(movies, collection_name):
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['movie_database']
    collection = db[collection_name]

    if movies:
        collection.insert_many(movies)
        print(f"Movies saved to MongoDb Collection {collection_name}")
    else:
        print(f"No movies to save to MongoDB collection '{collection_name}'")
