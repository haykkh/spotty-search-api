# -*- coding: utf-8 -*-
"""
    spotty_search.search.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask Blueprint for searching
"""

from flask import Blueprint, jsonify, Response
from spotty_search.api import spot
from spotty_search.search import fuzzy_search

# init Flask Blueprint at /search/ directory
search = Blueprint('search', __name__, url_prefix='/search')


@search.route('/', methods=['GET'])
def index() -> Response:
    return jsonify({'status': 'success'})


@search.route("/<query>")
def searcher(query: str) -> Response:
    results = fuzzy_search(query, spot.playlists_and_tracks)
    return jsonify(
        {
            spot.playlists[playlist_id].name: {
                'score': score,
                'playlist': spot.playlists[playlist_id]
            }
            for (score, playlist_id, data) in results
        }
    )


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


@search.route("playlistsandtracks")
def playlists_and_tracks() -> Response:
    """ Returns JSON with playlist id as key and tracks as elements
    """
    return jsonify(spot.playlists_and_tracks)


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
