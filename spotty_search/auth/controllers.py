from flask import Blueprint, redirect
from spotty_search.api import spt, client

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/')
def index():
    client.load_from_env()
    spt.client_creds = client
    if spt.is_oauth_ready:
        return redirect(spt.auth_uri(scopes=['playlist-read-private', 'playlist-read-collaborative']))
    else:
        return (
            jsonify(
                {
                    "error_description": "Client needs client_id, client_secret and a redirect uri in order to handle OAauth properly"
                }
            ),
            500,
        )