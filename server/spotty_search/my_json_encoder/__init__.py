from flask.json import JSONEncoder
from spotty_search.api import Playlist, Track

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Playlist):
            return {
                'id': obj.id, 
                'name': obj.name, 
                'tracks': obj.tracks, 
                'img': obj.img
                } 
        elif isinstance(obj, Track):
            return {
                'id': obj.id, 
                'name': obj.name, 
                'artists' : obj.artists,
                'album': obj.album
                } 
        return super(MyJSONEncoder, obj).default(obj)