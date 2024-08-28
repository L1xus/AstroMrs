from datetime import datetime

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
                movie['release_date'] = release_date.isoformat()
                movie['year'] = release_date.year
            except:
                pass
        
        final_movie_list.append(movie)

    return final_movie_list
