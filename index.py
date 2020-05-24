from gmusicapi import Mobileclient
from ytmusicapi import YTMusic

ytmusic_api = YTMusic('headers_auth.json')
#ytmusic_api.setup(filepath='headers_auth.json')

playmusic_api = Mobileclient()
playmusic_api.oauth_login('3d60a35b53065d86')

existing_playlists = ytmusic_api.get_library_playlists()
for playlist in playmusic_api.get_all_user_playlist_contents():
    dest_playlist = None
    already_added_songs = []
    matching = [s for s in existing_playlists if playlist['name'] in s['title']]
    if len(matching) < 1:
        dest_playlist = ytmusic_api.create_playlist(playlist['name'], "")
    else:
        dest_playlist = matching[0]['playlistId']
        already_added_songs = ytmusic_api.get_playlist(dest_playlist)['tracks']
    for song in playlist['tracks']:
        search_results = ytmusic_api.search(song['track']['artist'] + " " + song['track']['title'])
        if not any(search_results[0]['videoId'] in s['videoId'] for s in already_added_songs):
            ytmusic_api.add_playlist_items(dest_playlist, [search_results[0]['videoId']])
            print('Added song', search_results[0]['title'], "to", playlist['name'], 'playlist')



