from flask import Blueprint, render_template, redirect
from spotty_search.forms import SearchForm

search = Blueprint('search', __name__, url_prefix='/search')

@search.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return render_template('search/success.html')
    return render_template('search/index.html', form=form)