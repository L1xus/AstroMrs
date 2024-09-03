from dotenv import load_dotenv
import os
from src.fetch_movies import fetch_popular_movies, fetch_top_rated_movies, fetch_latest_movies
from src.transform_movies import validations_aka_transformation
from src.store_movies import save_movies_json, save_movies_mongo

load_dotenv()

api_url = os.getenv('API_URL')
authorization_key = os.getenv('AUTHORIZATION_KEY')

def fetch_all_movies():
    movies_list = []

    popular_movies = fetch_popular_movies(api_url, authorization_key)
    movies_list.extend(popular_movies)

    top_rated_movies = fetch_top_rated_movies(api_url, authorization_key)
    movies_list.extend(top_rated_movies)

    latest_movies = fetch_latest_movies(api_url, authorization_key)
    movies_list.extend(latest_movies)

    return movies_list


all_movies = fetch_all_movies()
print(f"All movies are fetched! {len(all_movies)}")

#final_movies_list = validations_aka_transformation(all_movies)
#print(f"Transformation don on your all_movies list: {len(final_movies_list)}")


#save_movies_json(final_movies_list, 'final_movies_list.json')
#save_movies_mongo(final_movies_list, 'final_movies_list')
