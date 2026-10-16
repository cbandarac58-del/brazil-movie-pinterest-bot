import os
import random
import requests

PINTEREST_ACCESS_TOKEN = os.getenv('PINTEREST_ACCESS_TOKEN')
PINTEREST_BOARD_ID = os.getenv('PINTEREST_BOARD_ID')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# උඹේ site එකේ link එක හෝ search URL එක මෙතනට දාන්න
MY_WEBSITE_BASE = "https://movies.vixtube.net/search?q="

def get_brazil_trending_movie():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}&language=pt-BR"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    movies = response.json().get('results', [])
    if not movies:
        return None
    return random.choice(movies)

def post_to_pinterest():
    movie = get_brazil_trending_movie()
    if not movie:
        print("No movie found.")
        return

    movie_title_pt = movie.get('title') or movie.get('original_title')
    overview = movie.get('overview', '')
    poster_path = movie.get('poster_path')
    release_date = movie.get('release_date', '')[:4]

    if not poster_path:
        return

    image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    encoded_title = requests.utils.quote(movie_title_pt)
    target_site_link = f"{MY_WEBSITE_BASE}{encoded_title}"

    pin_title = f"Assistir {movie_title_pt} ({release_date}) Online Grátis em HD"
    if not overview:
        overview = f"Assista ao filme {movie_title_pt} completo dublado e legendado online grátis em HD."

    pin_description = (
        f"{overview[:300]}... "
        f"Assista {movie_title_pt} grátis no nosso site! "
        f"#FilmesOnline #AssistirFilmes #{movie_title_pt.replace(' ', '')} #FilmesGratis #Dublado #HD"
    )

    url = "https://api.pinterest.com/v5/pins"
    headers = {
        "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "link": target_site_link,
        "title": pin_title[:100],
        "description": pin_description[:500],
        "board_id": PINTEREST_BOARD_ID,
        "media_source": {
            "source_type": "image_url",
            "url": image_url
        }
    }

    res = requests.post(url, json=payload, headers=headers)
    print("Status Code:", res.status_code)
    print("Pinterest Response:", res.json())

if __name__ == "__main__":
    post_to_pinterest()
