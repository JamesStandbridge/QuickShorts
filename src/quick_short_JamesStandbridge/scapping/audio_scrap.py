"""
This module contains the TikTokMusicScraper class which is used to scrape trending music data from TikTok's leaderboard 
website (https://tokboard.com/). It allows for extracting song metadata, downloading songs, and saving song metadata 
as JSON files. The module can be used as a script or imported as a Python module.

Classes:
    TikTokMusicScraper: Scrapes and downloads songs and their metadata from TikTok's leaderboard.

Functions:
    main(output_folder, number_of_songs): The main function to initiate scraping and downloading of songs.

Usage as a script:
    Run the script with the command line with optional arguments --output to specify the download directory 
    and --count to specify the number of songs to download.

    Example:
    `python audio_scrap.py --output my_music --count 5`
    This will download the top 5 trending songs and their metadata to the 'my_music' directory.

Usage as a module:
    Import the module and use the `TikTokMusicScraper` class in your own Python scripts.

    Example:
    ```python
    from audio_scrap import TikTokMusicScraper
    
    scraper = TikTokMusicScraper()
    data = scraper.scrape_music_trends()
    songs = scraper.extract_top_songs(data)
    for song in songs:
        scraper.download_mp3_with_metadata(song, 'path_to_output_directory')
    ```
"""


import requests
from bs4 import BeautifulSoup
import json
import os
import argparse

SCRAPPING_URL = 'https://tokboard.com/'
SCRIPT_DIV_ID = '__NEXT_DATA__'

class TikTokMusicScraper:
    def __init__(self, url=SCRAPPING_URL):
        """
        Initialize the TikTokMusicScraper with the provided URL.

        :param url: The URL to scrape music trends from (default is SCRAPPING_URL).
        """
        self.url = url

    def scrape_music_trends(self):
        """
        Scrape music trends from the specified URL and return the JSON data.

        :return: JSON data containing music trends.
        :raises: Exception if JSON data is not found in the script tag or if the webpage retrieval fails.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id=SCRIPT_DIV_ID)
            if script_tag:
                json_data = json.loads(script_tag.string)
                return json_data
            else:
                raise Exception("JSON data not found in the script tag.")
        else:
            raise Exception(f"Failed to retrieve the webpage, Status code: {response.status_code}")

    def extract_top_songs(self, json_data):
        """
        Extract the top songs from the provided JSON data.

        :param json_data: JSON data containing music trends.
        :return: List of dictionaries, each representing a top song.
        """
        songs = json_data['props']['pageProps']['songs']
        top_songs = []
        for song in songs[:10]:  
            tags = [tag[0] for tag in song['data']['tags']] if 'tags' in song['data'] else []
            song_dict = {
                'author': song['authorName'],
                'title': song['title'],
                'playUrl': song['playUrl'],
                'tags': tags
            }
            top_songs.append(song_dict)
        return top_songs
    

    def download_mp3(self, url, filename):
        """
        Download an MP3 file from the given URL and save it with the provided filename.

        :param url: URL of the MP3 file to download.
        :param filename: Name of the file to save.
        """
        try:
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024): 
                        if chunk:  
                            file.write(chunk)
                print(f"{filename} has been downloaded.")
            else:
                print(f"Failed to download the mp3. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while downloading the mp3: {e}")

    def download_mp3_with_metadata(self, song, output_folder):
        """
        Download an MP3 file with metadata for a song and save both the MP3 and 
        metadata in the specified output folder.

        :param song: Dictionary representing a song with metadata.
        :param output_folder: Folder where the MP3 and metadata should be saved.
        """
        song_title = song['title'].replace('/', '').replace('"', '')
        filename = f"{song_title}.mp3"
        filepath = os.path.join(output_folder, filename)
        self.download_mp3(song['playUrl'], filepath)
        metadata_filename = f"{song_title}.json"
        metadata_filepath = os.path.join(output_folder, metadata_filename)
        self.save_to_json(song, metadata_filepath)

    @staticmethod
    def save_to_json(data, filename='top_songs.json'):
        """
        Save data as JSON to the specified file.

        :param data: Data to be saved as JSON.
        :param filename: Name of the JSON file to save (default is 'top_songs.json').
        """
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)



def main(output_folder, number_of_songs):
    """
    Main function to download TikTok trending music and metadata.

    :param output_folder: Output folder for downloaded music and metadata.
    :param number_of_songs: Number of songs to download.
    """
    scraper = TikTokMusicScraper()
    try:
        json_data = scraper.scrape_music_trends()
        top_songs = scraper.extract_top_songs(json_data)[:number_of_songs]

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for song in top_songs:
            scraper.download_mp3_with_metadata(song, output_folder)

    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download TikTok trending music and metadata.')
    parser.add_argument('--output', type=str, default='output', help='Output folder for downloaded music and metadata.')
    parser.add_argument('--count', type=int, default=10, help='Number of songs to download.')
    args = parser.parse_args()

    main(args.output, args.count)

    