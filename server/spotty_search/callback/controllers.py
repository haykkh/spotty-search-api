"""
    spotty_search.callback.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask Blueprint for receiving callback from Spotify

    Redirects to /search/
    or returns error
"""

from typing import Union, Tuple
from flask import Blueprint, request, redirect, url_for, jsonify, abort, Response
from pyfy import AuthError
from spotty_search.api import spot
from werkzeug import wrappers

# init Flask Blueprint at /callback/ directory
callback = Blueprint('callback', __name__, url_prefix='/callback')


@callback.route('/spotify')
def spotify() -> Union[Tuple[Response, int], wrappers.Response]:
    """ Redirects to /search/ and initializes user's playlist data

        Returns:
            redirects to /search/ if no error returns from spotify
            otherwise returns errors
    """
    if request.args.get("error"):
        return jsonify(dict(error=request.args.get("error_description")))
    elif request.args.get("code"):
        grant = request.args.get("code")
        try:
            spot.spt.build_user_creds(grant=grant)
        except AuthError as e:
            return jsonify(dict(error_description=e.msg)), e.code
        else:
            spot.initdata()  # initialize user's playlist data
            return redirect(url_for("search.index"))
    else:
        return abort(500)
