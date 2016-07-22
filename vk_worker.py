import pickle
import re
import webbrowser
from datetime import datetime, timedelta
from urllib.parse import urlparse
from urllib.request import urlretrieve

import os
import vk

# id of vk.com application, that has access to audio
APP_ID = '5536060'
# if None, then save mp3 in current folder
MUSIC_FOLDER = 'music'
# file, where auth data is saved
AUTH_FILE = '.auth_data'
# chars to exclude from filename
FORBIDDEN_CHARS = '/\\\?%*:|"<>!'


def get_auth_params():
    auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                "&scope=audio&redirect_uri=http://oauth.vk.com/blank.html"
                "&display=page&response_type=token".format(app_id=APP_ID))
    webbrowser.open_new_tab(auth_url)
    redirected_url = input("Paste here url you were redirected:\n")
    aup = urlparse(redirected_url)
    fragment = aup.fragment
    user_token = re.split(r'&expires_in=', re.split(r'^access_token=', fragment)[1])[0]
    expires_in, user_id = re.split(r'&user_id=', re.split(r'&expires_in=', re.split(r'^access_token=', fragment)[1])[1])
    save_auth_params(user_token, expires_in, user_id)
    return user_token, user_id


def save_auth_params(access_token, expires_in, user_id):
    expires = datetime.now() + timedelta(seconds=int(expires_in))
    with open(AUTH_FILE, 'wb') as output:
        pickle.dump(access_token, output)
        pickle.dump(expires, output)
        pickle.dump(user_id, output)


def get_saved_auth_params():
    access_token = None
    user_id = None
    try:
        with open(AUTH_FILE, 'rb') as pkl_file:
            token = pickle.load(pkl_file)
            expires = pickle.load(pkl_file)
            uid = pickle.load(pkl_file)
        if datetime.now() < expires:
            access_token = token
            user_id = uid
    except IOError:
        pass
    return access_token, user_id


def download_track(t_url, t_name,music_folder=''):
    if not os.path.exists(music_folder):
        os.chmod(music_folder,777)
        os.makedirs(music_folder)
    t_path = os.path.join(music_folder or "", t_name)
    if not os.path.exists(t_path):
        print("Downloading {0}".format(t_name.encode('ascii', 'replace')))
        urlretrieve(t_url, t_path)


def get_track_from_spot(token,music_folder=''):
    session = vk.Session(access_token=token)

    vkapi = vk.API(session=session)
    with open('access_tok.txt') as f:
        for line in f:
            song_name, song_time = line.split("|:time|")
            song_time = divmod(divmod(int(song_time), 1000)[0], 60)
            result = vkapi.audio.search(q=song_name)
            if result[0]:
                for song in result[1:]:
                    if divmod(song['duration'], 60) == song_time:
                        print('YES')
                        # vkapi.audio.add(aid=song['aid'], owner_id=song['owner_id'])
                        download_track(song['url'], song['title'] + ".mp3",music_folder=music_folder)
                        break


def work(music_folder='music'):
    access_token, user_id = get_saved_auth_params()
    if not access_token or not user_id:
        access_token, user_id = get_auth_params()
    print(access_token, user_id)
    get_track_from_spot(access_token,music_folder=music_folder)
