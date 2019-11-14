# -*- coding: utf-8 -*-
"""
    test_auth
    ~~~~~~~~~

    pytest for /auth/
"""


def test_index(client):
    response = client.get('/auth/')

    assert response.status_code == 302
    assert response.headers['Location'][:52] == 'https://accounts.spotify.com/authorize?redirect_uri='
