import os
from flask import Flask, render_template
from pyfy import Spotify, ClientCreds, AuthError
from spotty_search.auth.controllers import auth
from spotty_search.callback.controllers import callback
from spotty_search.search.controllers import search

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_CONFIG'))
app.register_blueprint(search)
app.register_blueprint(auth)
app.register_blueprint(callback)

@app.route('/')
def index():
    return render_template('index.html')