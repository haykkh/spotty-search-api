from flask import Blueprint, jsonify, request
from spotty_search.api import spot

search = Blueprint('search', __name__, url_prefix='/search')

testing_data = []

@search.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'success'})

@search.route("/playlists")
def playlists():
    return jsonify(spot.playlists)

@search.route("/playlist/<id>")
def playlist(id):
    return jsonify(spot.playlists[id])

@search.route("/playlist/<id>/tracks")
def playlist_tracks(id):
    return jsonify([track for track in spot.playlists[id].tracks])


@search.route("old/playlists")
def old_playlists():
    return jsonify(spot.spt.user_playlists())

@search.route("old/playlist/<id>")
def old_playlist(id):
    return jsonify(spot.spt.playlist_tracks(id))

@search.route("old/playlist/<id>/tracks")
def old_playlist_tracks(id):
    return jsonify([track['track']['name'] for track in spot.spt.playlist_tracks(id)['items']])
