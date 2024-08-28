import requests

def fetch_movies(api_url, authorization_key, endpoint):
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

def fetch_popular_movies(api_url, authorization_key):
    return fetch_movies(api_url, authorization_key, '/movie/popular')

def fetch_top_rated_movies(api_url, authorization_key):
    return fetch_movies(api_url, authorization_key, '/movie/top_rated')

def fetch_latest_movies(api_url, authorization_key):
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

