from pyfy import Spotify, ClientCreds

class User:
    def __init__(self, s):
        self.spt = s


client = ClientCreds()
spot = User(Spotify())