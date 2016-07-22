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
    result_tuple = {}
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
        while songs_offset < songs_num:
            user_songs = sp.user_playlist_tracks(playlist_id=playlist_id, limit=songs_limit,
                                                 offset=songs_offset, user=user)
            for song in user_songs['items']:
                result_tuple[song['track']['name']] = [song['track']['duration_ms']]
                for artist in song['track']['artists']:
                    result_tuple[song['track']['name']].append(artist['name'])
            songs_offset += songs_limit

        print(result_tuple)
        with open('access_tok.txt', 'w') as f:
            for key, value in result_tuple.items():
                f.write("{0} {1}|:time|{2}\n".format(key, value[1], value[0]))

    else:
        print("Can't get token for", username)

