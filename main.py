import os

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']
SCOPE = "playlist-modify-private"


def get_top_100(date: str) -> list:
    bill_board_url = "https://www.billboard.com/charts/hot-100"
    response = requests.get(url=f"{bill_board_url}/{date}")
    soup = BeautifulSoup(response.text, "html.parser")
    songs = soup.find_all("h3", class_="a-no-trucate")
    song_names = [song.getText().strip() for song in songs]
    return song_names


def songs_add_playlist(song_names: list, date: str):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIPY_REDIRECT_URI,
                                                   scope=SCOPE,
                                                   show_dialog=True,
                                                   cache_path="token.txt"))
    user_id = sp.current_user()["id"]
    print(user_id)
    song_uris = []
    year = user_date.split("-")[0]
    for song in song_names:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        print(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    # Creating a new private playlist in Spotify
    playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
    print(playlist)

    # Adding songs found into the new playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


user_date = str(input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "))
songs = get_top_100(user_date)
songs_add_playlist(songs, user_date)
