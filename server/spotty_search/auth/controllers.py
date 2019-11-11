# -*- coding: utf-8 -*-
"""
    spotty_search.auth.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask Blueprint for authorizing user on Spotify

    Redirects to Spotify who then redirects to /callback/
    or returns 500 error
"""

from flask import Blueprint, redirect, jsonify, Response
from typing import Tuple, Union
from spotty_search.api import spot, client
from werkzeug import wrappers

# init Flask Blueprint at /auth/ directory
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/')
def index() -> Union[wrappers.Response, Tuple[Response, int]]:
    """ Authorizes user on Spotify

        If pyfy client is ready
            -> redirect to spotify user authentication requesting
              `playlist-read-private` and `playlist-read-collaborative`
               scopes
        else
            -> return 500 error

        Returns:
            redirects to spotify user authentication or returns 500 error
    """
    client.load_from_env()  # load client credentials from .env
    spot.spt.client_creds = client  # init client creds
    if spot.spt.is_oauth_ready:
        return redirect(spot.spt.auth_uri(
            scopes=['playlist-read-private', 'playlist-read-collaborative']))
    else:
        return (
            jsonify(
                {
                    "error_description": "Client needs client_id, client_secret and a redirect uri in order to handle OAauth properly"
                }
            ),
            500,
        )
