from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os

from src.fetch_movies import fetch_movies 
from src.transform_movies import validation_aka_transformation
from src.store_movies import save_movies_mongo

load_dotenv()
api_url = os.getenv('API_URL')
authorization_key = os.getenv('AUTHORIZATION_KEY')

spark = SparkSession.builder.master("spark://spark-master:7077").appName("Movies Pipeline").getOrCreate()


def etl(endpoint, total_pages=None, filename=None):
    if endpoint == '/movie/latest':
        movies = fetch_movies(api_url, authorization_key, endpoint)
        transformed_movies = validation_aka_transformation(movies)
        save_movies_mongo(transformed_movies, 'movies_collection')
    else:
        pages = list(range(1, total_pages + 1))
        rdd = spark.sparkContext.parallelize(pages, len(pages))

        rdd.foreach(lambda page: 
            save_movies_mongo(
                validation_aka_transformation(
                    fetch_movies(api_url, authorization_key, endpoint, page)
                ),
                filename
            )
        )
    print(f"ETL process completed for {endpoint}")


etl('/movie/popular', 500, 'movies_collection')
etl('/movie/top_rated', 500, 'movies_collection')
etl('/movie/latest')
