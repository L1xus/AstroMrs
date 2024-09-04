import json
from pymongo import MongoClient

def save_movies_jsonl(movies, filename):
    with open(filename, 'a', encoding='utf-8') as file: 
        for movie in movies:
            file.write(json.dumps(movie, ensure_ascii=False, indent=4) + '\n')
    print(f"{len(movies)} Movies appended to {filename}")

def save_movies_mongo(movies, collection_name):
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['movie_database']
    collection = db[collection_name]

    if movies:
        collection.insert_many(movies)
        print(f"Movies saved to MongoDb Collection {collection_name}")
    else:
        print(f"No movies to save to MongoDB collection '{collection_name}'")
