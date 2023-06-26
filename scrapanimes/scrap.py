import requests
import re
from bs4 import BeautifulSoup
import utils
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
url_template = "https://o.anime-slayer.com/مسلسلات-انمي/page/{}"

# find the last page number
response_last = requests.get(url_template.format(1), headers=headers)
soup_last = BeautifulSoup(response_last.content, "html.parser")
last_page_link = soup_last.find_all("a", class_="page-numbers")[-2].get("href")
last_page_number = int(re.search(r'\d+', last_page_link.split('/')[-1]).group())


# Function to save the page number to a file
def save_page_number(page_number):
    with open("scrapanimes/index.json", "w") as file:
        file.write(str(page_number))


# Function to load the page number from a file
def load_page_number():
    try:
        with open("scrapanimes/index.json", "r") as file:
            page_number = int(file.read())
    except FileNotFoundError:
        page_number = 0
    return page_number


page_number = load_page_number()



anime_list = []

for page_number in range(last_page_number, 0, -1):
    url = url_template.format(page_number)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    anime_cards = soup.find_all("div", class_="anime-card-container")

    if not anime_cards:
        continue

    for card in anime_cards:
        url_anime = card.find("a", class_="overlay").get("href")
        time.sleep(1)
        # get the MAL link from the anime page
        response_anime = requests.get(url_anime, headers=headers)
        soup_anime = BeautifulSoup(response_anime.content, "html.parser")
        description = soup_anime.find("p", class_="anime-story")
        mal_link = soup_anime.find("a", class_="anime-mal")
        if mal_link is None:
            continue
        mal_id_match = re.search(r'\d+', mal_link.get("href"))
        if mal_id_match is None:
            continue
        mal_id = mal_id_match.group()
        save_page_number(page_number)
        # fetch anime data from Jikan API V4
        url_jikan = f"https://api.jikan.moe/v4/anime/{mal_id}"
        response_jikan = requests.get(url_jikan, headers=headers)
        if response_jikan.status_code == 200:
            data_jikan = response_jikan.json()
            if "data" in data_jikan:
                # extract relevant data
                title = data_jikan["data"]["title"]
                title_english = data_jikan["data"]["title_english"]
                episodes = data_jikan["data"]["episodes"]
                score = data_jikan["data"]["score"]
                img = data_jikan["data"]["images"]['jpg']['image_url']
                rank = data_jikan["data"]["rank"]
                genres = [genre['name'] for genre in data_jikan["data"]["genres"]]  # get list of genre names
                popularity = data_jikan["data"]["popularity"]
                synopsis = description.text
                genres_str = ", ".join(genres)
                rating = data_jikan["data"]["rating"]
                year = data_jikan["data"]["year"]
                type = data_jikan["data"]["type"]
                airing = data_jikan["data"]["airing"]
                created_at = data_jikan["data"]["aired"]["from"].split("T")[0]
                season = data_jikan["data"]["season"]
                select_query = f"SELECT mal_id FROM anime WHERE mal_id = {mal_id}"
                print(title)
                data = utils.select("animes", condition_dict={"mal_id": mal_id})
                if len(data) > 0:
                    print('Already Exist')
                else:
                    data_dict = {
                        "mal_id": mal_id,
                        "title": title,
                        "title_english" : title_english,
                        "episodes": episodes,
                        "score": score,
                        "img": img,
                        "rank": rank,
                        "popularity": popularity,
                        "synopsis": synopsis,
                        "genres": genres_str,
                        "rating": rating,
                        "year": year,
                        "type": type,
                        "airing": airing,
                        "created_at": created_at,
                        "season": season
                    }
                    print('success insert')
                    result = utils.insert("animes", data_dict)

    # decrement page number to crawl pages in reverse order
    print(page_number)
    page_number -= 1
    # exit the loop if page number is zero
    if page_number == 0:
        break
    # sleep for 1 second before making the next request
    time.sleep(1)



