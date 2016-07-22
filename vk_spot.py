from spotify_worker import work as spotwork
from vk_worker import work as vkwork

# your username in spotify
USERNAME = 'Artem Kryvonis'

# copy playlist url form spotify and paste here
PLAYLIST_URL = 'https://open.spotify.com/user/spotify/playlist/7tIim3qlaUUT1vXe43VlAA'
# folder where you find your music
FOLDER = '/Volumes/myfoldartem/NuMetal'

spotwork(playlist_url=PLAYLIST_URL, username=USERNAME)
vkwork(music_folder=FOLDER)

