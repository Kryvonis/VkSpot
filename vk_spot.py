from vk_worker import work as vkwork
from spotify_worker import work as spotwork


# your username in spotify
USERNAME = 'Artem Kryvonis'

# copy playlist url form spotify and paste here
# PLAYLIST_URL = 'https://open.spotify.com/user/spotifydiscover/playlist/6TQuzFJVbuiL5W5iHjU4sX' #weekly
PLAYLIST_URL = 'https://open.spotify.com/user/spotify/playlist/5T4KBJYQt9oQYrLgkgaQFW'

# folder where you find your music
# FOLDER = '/Volumes/Kryvonis/music/weekly'
FOLDER = '/Volumes/Kryvonis/music/saved'

spotwork(playlist_url=PLAYLIST_URL, username=USERNAME)
vkwork(music_folder=FOLDER)
