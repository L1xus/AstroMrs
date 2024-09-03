from dotenv import load_dotenv
import os
import json

from src.fetch_movies import fetch_popular_movies, fetch_top_rated_movies, fetch_latest_movies
from src.transform_movies import validations_aka_transformation
from src.store_movies import save_movies_json, save_movies_mongo

from pyspark.sql import SparkSession

load_dotenv()

api_url = os.getenv('API_URL')
authorization_key = os.getenv('AUTHORIZATION_KEY')

spark = SparkSession.builder.master("local").appName("Movies Pipeline").getOrCreate()

fetch_functions = [
    lambda: fetch_popular_movies(api_url, authorization_key),
    lambda: fetch_top_rated_movies(api_url, authorization_key),
    lambda: fetch_latest_movies(api_url, authorization_key)
]

def fetch_movies_parallel():
    rdd = spark.sparkContext.parallelize(fetch_functions, len(fetch_functions))
    movies_rdd = rdd.flatMap(lambda f: f())
    return movies_rdd.collect()

movies = fetch_movies_parallel()
print(f"all movies are fetched with help of pyspark :) {len(movies)}")
