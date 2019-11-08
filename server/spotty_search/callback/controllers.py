from flask import Blueprint, request, redirect, url_for, jsonify, abort
from pyfy import AuthError
from spotty_search.api import spot

callback = Blueprint('callback', __name__, url_prefix='/callback')

@callback.route('/spotify')
def spotify():
    if request.args.get("error"):
        return jsonify(dict(error=request.args.get("error_description")))
    elif request.args.get("code"):
        grant = request.args.get("code")
        try:
            user_creds = spot.spt.build_user_creds(grant=grant)
        except AuthError as e:
            return jsonify(dict(error_description=e.msg)), e.code
        else:
            return redirect(url_for("search.index"))
    else:
        return abort(500)