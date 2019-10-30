from flask import Flask, render_template
from spotty_search.search.controllers import search
import os

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_CONFIG'))
app.register_blueprint(search)

@app.route('/')
def index():
    return render_template('index.html')