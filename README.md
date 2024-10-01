## Overview
This repository contains a personal project aimed at enhancing my skills in Data Engineering. The project involves building a data pipeline that extracts data from an API, transforms it, and loads it into a mongodb database.
I use Spark to distribute this process and Airflow to automate it.

> [!IMPORTANT]
> This project is made for the sake of practicing and learning

## Table of Contents
* [Architecture diagram](#architecture-diagram)
* [How it works](#how-it-works)
* [Tech Stack](#teck-stack)
* [Prerequisites](#prerequisites)
* [Run the project](#run-the-project)
* [References](#references)
* [Contributions](#contributions)

## Architecture diagram
*Will add this later* 

## How it works

1. ### Extract
The **extract** phase is handled by the function fetch_movies from src/fetch_movies.py module.
 - API Requests: The fetch_movies function sends GET requests to TMDB API endpoints.
 - Spark Integration: For endpoints with multiple pages, the script uses Spark's RDD to distribute the API calls across 2 spark-workers.

2. ### Transform
The **transform** phase involves the function validation_aka_transformation from src/transform_movies.py module.
 - Data Cleaning: The validation_aka_transformation function performs data cleaning on the fetched movies by removing duplicates, unwanted fields and null values.
 - Data Transformation: The function also transforms the release_date to datetime and creates a year field.

3. ### Load 
The **load** phase is execute by the save_movies_mongo function from src/store_movies.py module.
 - Storage in MongoDB: After validation, the transformed movies is loaded into a MongoDB Collection (movies_collection).

- **Those 3 ETL functions are called within a spark job to speed up the process of extracting, transforming and loading large volumes of movies.**

- **Apache Airflow is used to automate and orchestrate the spark job, enabling scheduled execution and efficient management of the ETF workflow.**

## Tech Stack
 - **Python:** Main programming language used for building the ETL pipeline logic.
 - **Docker & Docker-Compose:** Containerizes the application, manage services like Spark, Airflow, MongoDB.
 - **Apache Airflow:** Automate and scheduled the ETL workflow.
 - **PySpark:** Handles distributed data processing for the ETL.
 - **MongoDB:** NoSQL database to store the transformed movies.

## Prerequisites
To run the project you need:
 - [Docker](https://docs.docker.com/get-docker/) - You must allocate a minimum of 8 GB of Docker memory resource.
 - [Python 3.8+ (pip)](https://www.python.org/)
 - [docker-compose](https://docs.docker.com/compose/install/)
 - [TMDB API Keys](https://developer.themoviedb.org/docs/getting-started)

## Run the project

```docker-compose up airflow-init```

```docker-compose up --build```

In Airflow webserver (Admin >> Connections) you'll need to create a spark connection.

## References
 * [TMDB API Documentation](https://developer.themoviedb.org/docs/getting-started)
 * [RDD vs DataFrame : The Deference!](https://www.linkedin.com/pulse/rdd-vs-dataframe-deference-soumya-sankar-panda-dplzc/?trackingId=KJPTpfQAQEGT1o8e1EADsg%3D%3D)
 * [Spark Documentation](https://spark.apache.org/docs/latest/)
 * [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/index.html)
 * [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user)
 * [Apache Airflow Tutorial: Architecture, Concepts, and How to Run Airflow Locally With Docker](https://devblogit.com/apache-airflow-tutorial-architecture-concepts-and-how-to-run-airflow-locally-with-docker)
 * [How to Schedule and Automate Spark Jobs Using Apache Airflow](https://devblogit.com/how-to-schedule-and-automate-spark-jobs-using-apache-airflow)
## Contributions
Feel free to submit a pull request or report issues. Contributions are welcome to make this project even better!
