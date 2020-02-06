# -*- coding: utf-8 -*-
"""
    spotty_search.my_json_encoder
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Custom flask JSON encoder

    Serializes:
        spotty_search.Playlist
        spotty_search.Track
"""

from flask.json import JSONEncoder
from spotty_search.api import Playlist, Track
from typing import Union, Dict, Any


class MyJSONEncoder(JSONEncoder):
    """ Custom flask JSON encoder

        Serializes:
            spotty_search.Playlist
            spotty_search.Track
    """
    def default(self, obj: Union[Playlist, Track]) -> Dict[str, Any]:
        """ Serializes spotty_search.Playlist & spotty_search.Track types
        """
        if isinstance(obj, Playlist):
            return {
                'id': obj.id,
                'name': obj.name,
                'tracks': obj.tracks,
                'number_of_tracks': obj.number_of_tracks,
                'img': obj.img,
                'uri': obj.uri
            }
        elif isinstance(obj, Track):
            return {
                'id': obj.id,
                'name': obj.name,
                'artists': obj.artists,
                'album': obj.album
                }
        return super(MyJSONEncoder, obj).default(obj)
