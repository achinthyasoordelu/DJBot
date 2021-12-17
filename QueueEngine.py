import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


redirect_uri="http://localhost:8888/callback"
CLIENT_ID = "2808262b243e4e1a84ba6f3acc329e2e"
CLIENT_SECRET_ID = "fa6008fb6c4047969d1ecea6bd3ee494"
achinvitha = '122370070'
playlist = '0NKLGjquFsRAI24rMHXQse'

def instantiateSpotify():
    # Authenticate as myself
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET_ID)
    token = util.prompt_for_user_token(achinvitha,
                                       scope='playlist-modify-public playlist-modify-private streaming user-read-currently-playing user-read-playback-state',
                                       client_id=CLIENT_ID, client_secret=CLIENT_SECRET_ID,
                                       redirect_uri="http://localhost:8888/callback")
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth=token) #authenticate sp object as myself

def songStatus():
    sp = instantiateSpotify()
    return sp.current_playback()['item']['uri']

def queueSong(song_uri, numQueue):
    i = 0
    sp = instantiateSpotify()
    songs = sp.user_playlist(achinvitha, playlist_id=playlist, fields="tracks,next")
    currentSongURI = sp.current_playback()['item']['uri']
    for i, item in enumerate(songs['tracks']['items']):
        if currentSongURI == item['track']['uri']:
            break
    results = sp.user_playlist_add_tracks(achinvitha, playlist, ['spotify:track:' + song_uri], position= i + 1 + numQueue) #add song to top of queue (if unshuffled)
    songs = sp.user_playlist(achinvitha, playlist_id=playlist, fields="tracks,next")
    track = sp.track(['spotify:track:' + song_uri])
    return track['name'], numQueue + 1

def playlistData():
    tracklist = []
    sp = instantiateSpotify()
    songs = sp.user_playlist(achinvitha, playlist_id=playlist, fields="tracks,next")
    currentSongURI = sp.current_playback()['item']['uri']
    for item in songs['tracks']['items']:
        tracklist += [item['track']['uri']]
    return tracklist

def removeSong(song_uri, numQueue):
    sp = instantiateSpotify()
    track = sp.track(['spotify:track:' + song_uri])
    songs = sp.user_playlist(achinvitha, playlist_id=playlist, fields="tracks,next")
    results = sp.user_playlist_remove_all_occurrences_of_tracks(user=achinvitha, playlist_id=playlist, tracks=['spotify:track:' + song_uri])
    return track['name'], numQueue - 1

def clearPlaylist():
    #Used in reset command to clear playlist except for last song on the list
    sp = instantiateSpotify()
    songs = sp.user_playlist(achinvitha, playlist_id=playlist, fields="tracks,next")
    for i, item in enumerate(songs['tracks']['items']):
        sp.user_playlist_remove_all_occurrences_of_tracks(achinvitha, playlist, ['spotify:track:' + item['track']['uri']])
    sp.user_playlist_add_tracks(achinvitha, playlist, ['spotify:track:' + item['track']['uri']])


if __name__ == "__main__":
    print(queueSong("47l9wxr6RwgoTSfnseBRcf", 0))

