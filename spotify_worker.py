import spotipy
import spotipy.util as util

scope = 'user-library-read'


def work(playlist_url='https://open.spotify.com/user/ab0o/playlist/0Au1T5jRUGDV0TO0M0EJMn',
         username=""):
    token = util.prompt_for_user_token(username,
                                       client_id='5a02a6cdbb4d4c739ba8dd8633627baf',
                                       client_secret='2017480ec40c41b3a83b70761091808a',
                                       redirect_uri='http://oauth.vk.com/blank.html',
                                       scope=scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        user = playlist_url.split('/user/')[1].split('/playlist')[0]
        playlist_id = playlist_url.split('/playlist/')[1]
        sp.trace = False

        songs_limit = 50
        songs_offset = 0
        user_songs = sp.user_playlist_tracks(playlist_id=playlist_id, limit=songs_limit,
                                             offset=songs_offset, user=user)
        songs_num = user_songs['total']
        with open('access_tok.txt', 'w') as f:
            while songs_offset < songs_num:
                user_songs = sp.user_playlist_tracks(playlist_id=playlist_id, limit=songs_limit,
                                                     offset=songs_offset, user=user)
                list_song = user_songs['items']
                for song in user_songs['items']:
                    song_name = song['track']['name']
                    song_duration = song['track']['duration_ms']
                    song_artist = []
                    for artist in song['track']['artists']:
                        song_artist.append(artist['name'])
                    f.write("{0} {1}|:time|{2}\n".format(song_name, song_artist[0], song_duration))
                songs_offset += songs_limit

    else:
        print("Can't get token for", username)
