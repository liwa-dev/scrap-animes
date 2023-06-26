# Anime Scrapping

# Description

'scrap-animes' is an efficient and user-friendly script for scraping anime data. It simplifies retrieving titles, genres, ratings, and summaries from online sources. Whether you're a researcher or a developer, 'scrap-animes' provides a reliable solution for comprehensive and up-to-date anime information.

The script includes an auto-save feature that saves the last scrapping website on `index.json`. When the script is restarted, it will continue counting from where it left off.

## Installation

1. Clone the repository: `git clone https://github.com/liwa-dev/anime-scrapping`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create an account on [Supabase](https://supabase.io/) and create a new project.
4. In your Supabase project, create a new table called `animes` with the following columns:
   * `mal_id` (integer) - this column is used to store the MyAnimeList ID of the anime
   * `title` (string) - this column is used to store the title of the anime
   * `title_english` (string) - this column is used to store the English title of the anime
   * `episodes` (integer) - this column is used to store the number of episodes
   * `score` (float) - this column is used to store the score of the anime
   * `img` (string) - this column is used to store the image URL of the anime
   * `rank` (integer) - this column is used to store the rank of the anime
   * `popularity` (integer) - this column is used to store the popularity rank of the anime
   * `synopsis` (string) - this column is used to store the synopsis of the anime
   * `genres` (string) - this column is used to store the genres of the anime
   * `rating` (string) - this column is used to store the rating of the anime
   * `year` (integer) - this column is used to store the year the anime aired
   * `type` (string) - this column is used to store the type of the anime
   * `airing` (boolean) - this column is used to store whether the anime is currently airing or not
   * `created_at` (datetime) - this column is used to store the timestamp of when the anime data was scraped
   * `season` (string) - this column is used to store the season the anime belongs to
5. In your Supabase project, create a new table called `servers` with the following columns (this for scrapepisodes):
   * `link_server` (string) - this column is used to store the link to the streaming server
   * `server_name` (string) - this column is used to store the name of the streaming server
   * `mal_id` (integer) - this column is used to store the MyAnimeList ID of the anime being streamed
   * `Episode` (string) - this column is used to store the name of the episode being streamed
6. Go to the `Settings` tab in your Supabase project and copy your `API URL` and `API Key`.
7. Paste the `API URL` and `API Key` in the `utils.py` file, under the `SUPABASE_URL` and `SUPABASE_KEY` constants, respectively.

## Usage

To use the script, simply run python `scrap.py` in your terminal. The script will start scraping the desired site and save the relevant information to your Supabase table.

If you prefer to use a different database, you can modify both files `utils.py` , `scrap.py` to use your own API.

## Contributing

If you'd like to contribute to the project, feel free to submit a pull request or open an issue. We'd love to hear your feedback and suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
