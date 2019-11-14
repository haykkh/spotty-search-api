# -*- coding: utf-8 -*-
"""
    test_api
    ~~~~~~~~

    pytest for api
"""

import spotty_search.api
from pyfy import Spotify, ClientCreds


def test_catcher():
    passer = {
        'images': [
            {
                'url': 'www'
            }]}

    failer = {'images': []}

    assert spotty_search.api.catcher(passer) == 'www'
    assert spotty_search.api.catcher(failer) == None


def test_initdata(client):
    cl = ClientCreds()
    spot = spotty_search.api.User(Spotify())

    client.get('/auth/')

    spot.initdata()
