import json
from pymongo import MongoClient

def check_dup(file_path):
    ids = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            movie = json.loads(line)
            ids.append(movie['id'])
    return ids

def save_movies_jsonl(movies, filename):
    movie_ids = check_dup(filename)
    with open(filename, 'a', encoding='utf-8') as file: 
        for movie in movies:
            if movie['id'] not in movie_ids:   
                file.write(json.dumps(movie, ensure_ascii=False) + '\n')
                movie_ids.append(movie['id']) 
    print(f"{len(movies)} new Movies appended to {filename}")

def save_movies_mongo(movies, collection_name):
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['movie_database']
    collection = db[collection_name]

    if movies:
        collection.insert_many(movies)
        print(f"Movies saved to MongoDb Collection {collection_name}")
    else:
        print(f"No movies to save to MongoDB collection '{collection_name}'")
