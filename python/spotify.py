import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import calendar

SPOTIPY_CLIENT_ID = '055fc216f50c4675a442840a6ee93918'
SPOTIPY_CLIENT_SECRET = 'eb69f02600694346bad03a0fcfd6449d'
scope = "playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative"

def makeUserPlaylist(username, playlistName):
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope, username=username, redirect_uri='https://www.google.com', client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

    if auth_manager:
        sp = spotipy.Spotify(auth_manager=auth_manager)
        results = sp.current_user_playlists()
        playlists = results['items']
        list = []
        for result in playlists:
            list += [result['name']]
        if playlistName not in list:
            newPlaylist = sp.user_playlist_create(user = username, name=playlistName)
            return newPlaylist["id"]
        else:
            for i in playlists:
                if i["name"] == playlistName:
                    playlistID = i["id"]
                    return playlistID
    else:
        print("Can't get token for", username)

def addUserPlaylistTracks(id, username, tracks):
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope, username=username, redirect_uri='https://www.google.com', client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

    existingTracks = getPlaylistTracks(id, username, auth_manager)
    newTracks = []
    for i in tracks:
        if i not in existingTracks:
            newTracks.append(i)

    if auth_manager:
        sp = spotipy.Spotify(auth_manager=auth_manager)
        if newTracks:
            sp.playlist_add_items(playlist_id = id, items=newTracks) # only add track if isnt already in the playlist
    else:
        print("Can't get token for", username)

def getPlaylistTracks(id, username, manager):
    # auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope, username=username, redirect_uri='https://www.google.com', client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

    if manager:
        sp = spotipy.Spotify(auth_manager=manager)
        yo = sp.playlist_items(playlist_id = id)
        yo = yo['items']
        uris = []
        for i in yo:
            uris.append(i['track']['uri'])
        return uris

def getTopTracks(artist):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_secret=SPOTIPY_CLIENT_SECRET, client_id=SPOTIPY_CLIENT_ID))
    results = spotify.search(q=artist, type="artist")
    # print(results['artists']['total'])
    artists = results['artists']['items']
    # for result in artists:
    #     print(result['name'])

    if artists:
        url = artists[0]['external_urls'].get("spotify")
        results = spotify.artist_top_tracks(url)

        tracksURI = []
        tracksNames = []
        for track in results['tracks'][:1]:
            trackuri = track["uri"]
            trackname = track["name"]
            # trackurl = track['external_urls'].get("spotify")
            tracksURI.append(trackuri)
            tracksNames.append(trackname)
        return tracksURI, tracksNames
    else:
        #print("Artist not found!")
        return None

def buildPlaylist(artists, playlistID, username):
    for i in artists:
        tracks = getTopTracks(i)
        if tracks is not None:
            trackuris, trackname = tracks
            addUserPlaylistTracks(playlistID, username, trackuris)

if __name__ == '__main__':
    trackuris, trackname = getTopTracks('black keys')
    playlistID = makeUserPlaylist("nickcres13","Bay Area", 7)
    addUserPlaylistTracks(playlistID, "nickcres13", trackuris)

    tracks = getPlaylistTracks(playlistID, "nickcres13")
    print(type(tracks))
    'https://open.spotify.com/track/5G1sTBGbZT5o4PNRc75RKI'

