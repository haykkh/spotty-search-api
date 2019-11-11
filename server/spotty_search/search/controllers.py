# -*- coding: utf-8 -*-
"""
    spotty_search.search.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask Blueprint for searching
    `Brains` of the whole operation
"""

from flask import Blueprint, jsonify, Response
from spotty_search.api import spot

# init Flask Blueprint at /search/ directory
search = Blueprint('search', __name__, url_prefix='/search')


@search.route('/', methods=['GET'])
def index() -> Response:
    return jsonify({'status': 'success'})


@search.route("/playlists")
def playlists() -> Response:
    """ Returns JSON of user's playlists
    """
    return jsonify(spot.playlists)


@search.route("/playlist/<id>")
def playlist(id: str) -> Response:
    """ Returns JSON of `id` playlist's info
    """
    return jsonify(spot.playlists[id])


@search.route("/playlist/<id>/tracks")
def playlist_tracks(id: str) -> Response:
    """ Returns tracks in `id` playlist
    """
    return jsonify([track for track in spot.playlists[id].tracks])


"""
    ************************************
    **                                **
    **  returning raw json from pyfy  **
    **                                **
    ************************************
"""


@search.route("old/playlists")
def old_playlists() -> Response:
    """ Returns user's playlists
    """
    return jsonify(spot.spt.user_playlists())


@search.route("old/playlist/<id>")
def old_playlist(id: str) -> Response:
    """ Returns JSON of `id` playlist's info
    """
    return jsonify(spot.spt.playlist_tracks(id))


@search.route("old/playlist/<id>/tracks")
def old_playlist_tracks(id: str) -> Response:
    """ Returns tracks in `id` playlist
    """
    return jsonify([
        track['track']['name']
        for track
        in spot.spt.playlist_tracks(id)['items']
        ])
