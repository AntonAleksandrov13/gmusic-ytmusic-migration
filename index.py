from gmusicapi import Mobileclient
from ytmusicapi import YTMusic
import sys
from os import path
import time
from threading import Thread


def move_play_lists(ytmusic_api, playmusic_api):
    threads = []
    existing_playlists = ytmusic_api.get_library_playlists()
    for playlist in playmusic_api.get_all_user_playlist_contents():
        thread = Thread(target=move_play_list, args=(existing_playlists, playlist))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print('All playlistis are synced')


def move_play_list(existing_playlists, playlist):
    dest_playlist = None
    already_added_songs = []
    matching = [s for s in existing_playlists if playlist['name'] in s['title']]
    if len(matching) < 1:
        dest_playlist = ytmusic_api.create_playlist(playlist['name'], "")
    else:
        dest_playlist = matching[0]['playlistId']
        already_added_songs = ytmusic_api.get_playlist(dest_playlist)['tracks']
    for song in playlist['tracks']:
        try:
            search_results = ytmusic_api.search(song['track']['artist'] + " " + song['track']['title'])
            if not any(search_results[0]['videoId'] in s['videoId'] for s in already_added_songs):
                ytmusic_api.add_playlist_items(dest_playlist, [search_results[0]['videoId']])
                print('Added song', search_results[0]['title'], "to", playlist['name'], 'playlist')
        except:
            print('Could not find')
    time.sleep(5)

args = sys.argv
print('It`s required that you login in the both services')
auth_ytmusic = ''
device_id_playmusic = ''
if len(args) == 3:
    device_id_playmusic = args[1]
    auth_ytmusic = args[2]
else:
    device_id_playmusic = args[1]

playmusic_api = Mobileclient()
playmusic_api.perform_oauth()
playmusic_api.oauth_login(device_id_playmusic)

ytmusic_api = None
if path.exists(auth_ytmusic):
    print('You have provided a json file. YouTube Music will try to login in with it')
    ytmusic_api = YTMusic(auth_ytmusic)
else:
    print(
        'YouTube Music authentication is done by visiting youtube.music.com in Firefox and copying request headers of '
        'a '
        'Post request. You will need to paste this content below')
    ytmusic_api = YTMusic()
    ytmusic_api.setup(filepath='headers_auth.json')
move_play_lists(ytmusic_api, playmusic_api)
