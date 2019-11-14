# -*- coding: utf-8 -*-
"""
    test_root
    ~~~~~~~~~

    pytest for index
"""


def test_index(client):
    assert client.get("/").status_code == 200
