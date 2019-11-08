from pyfy import Spotify, ClientCreds

def catcher(obj):
    try:
        return obj['images'][0]['url']
    except IndexError:
        return None

class Track:
    def __init__(self, i, n, ar, al):
        self.id = i
        self.name = n
        self.artists = ar
        self.album = al

class Playlist:
    def __init__(self, i, n, t, u):
        self.id = i
        self.name = n
        self.tracks = t
        self.img = u


class User:
    def __init__(self, s):
        self.spt = s

    def initData(self):
        self.number_of_playlists = self.spt.user_playlists()['total']
        self.playlists = {}
        i = 0
        while i * 50 < self.number_of_playlists:
            print(f'i * 50: {i * 50}')
            self.playlists.update({
                playlist['id'] :
                Playlist(
                    playlist['id'], 
                    playlist['name'], 
                    [
                        Track(
                            track['track']['id'],
                            track['track']['name'], 
                            [
                                artist['name']
                                for artist
                                in track['track']['artists']
                            ],
                            track['track']['album']['name']
                            )
                        for track
                        in self.spt.playlist_tracks(playlist['id'])['items']
                    ],
                    catcher(playlist)
                    ) 
                for playlist 
                in self.spt.user_playlists(spot.spt.user_creds.id, 50, i * 50)['items']
            })
            i += 1
 

client = ClientCreds()
spot = User(Spotify())