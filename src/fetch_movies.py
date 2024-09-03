import requests

def fetch_movies(api_url, authorization_key, endpoint, page=None):
    page_movies = []
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization_key}"
    }

    if page:
        page_url = f"{api_url}{endpoint}?language=en-US&page={page}"
    else:
        page_url = f"{api_url}{endpoint}"

    response = requests.get(page_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if endpoint == '/movie/latest':
            return [data]
        else:
            movies = data.get('results', [])
            page_movies.extend(movies)
            return page_movies
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")
        return []

