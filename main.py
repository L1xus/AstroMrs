from dotenv import load_dotenv
import os
import requests
import json
from pymongo import MongoClient

load_dotenv()

api_url = os.getenv('API_URL')
authorization_key = os.getenv('AUTHORIZATION_KEY')

def fetch_movies(endpoint):
    all_movies = []
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization_key}"
    }

    for page in range(1, 501):
        page_url = f"{api_url}{endpoint}?language=en-US&page={page}"
        response = requests.get(page_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
            all_movies.extend(movies)

        else:
            print(f"Failed to fetch page {page}: {response.status_code}")
            break

    return all_movies

def fetch_popular_movies():
    return fetch_movies('/movie/popular')

def fetch_top_rated_movies():
    return fetch_movies('/movie/top_rated')

def fetch_latest_movies():
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization_key}"
    }
    url = f"{api_url}/movie/latest"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        latest_movie = response.json()
        return [latest_movie]
    else:
        print(f"Failed to fetch the latest movie: {response.status_code}")
        return []

def fetched_movies():
    fetched_movies = []

    popular_movies = fetch_popular_movies()
    fetched_movies.extend(popular_movies)

    top_rated_movies = fetch_top_rated_movies()
    fetched_movies.extend(top_rated_movies)

    latest_movies = fetch_latest_movies()
    fetched_movies.extend(latest_movies)

    return fetched_movies

def validations_aka_transformation(movies):
    final_movie_list = []
    seen_movie_ids = set()

    for movie in movies:
        # Remove duplications
        movie_id = movie.get('id')
        if not movie_id or movie_id in seen_movie_ids:
            continue
        seen_movie_ids.add(movie_id)

        # Remove unwanted fields
        for field in ['backdrop_path', 'poster_path', 'original_title']:
            movie.pop(field, None)

        # Remove Null values
        if any(value is None or value == '' for value in movie.values()):
            continue

        # Convert release_date to datetime && extract year
        if 'release_date' in movie:
            try:
                release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')
                movie['release_date'] = release_date
                movie['year'] = release_date.year
            except:
                pass
        
        final_movie_list.append(movie)

    return final_movie_list

all_movies = fetched_movies()
print(f"All movies are fetched! {len(all_movies)}")

final_movies_list = validations_aka_transformation(all_movies)
print(f"Transformation don on your all_movies list: {len(final_movies_list)}")

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

save_movies_json(final_movies_list, 'final_movies_list.json')
save_movies_mongo(final_movies_list, 'final_movies_list')
