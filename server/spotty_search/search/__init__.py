# -*- coding: utf-8 -*-
"""
    spotty_search.search
    ~~~~~~~~~~~~~~~~~~~~

"""

from fuzzywuzzy import fuzz, process


def fuzzy_search(x, choices):
    results = process.extractBests(
        x, choices=choices, scorer=fuzz.token_set_ratio, score_cutoff=90, limit=None
    )
    return [
        (score, playlist_id) for (data, score, playlist_id) in results
    ]
