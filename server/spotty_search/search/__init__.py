# -*- coding: utf-8 -*-
"""
    spotty_search.search
    ~~~~~~~~~~~~~~~~~~~~

    Fuzzy searches through all playlists for matches using fuzzywuzzy
"""

from fuzzywuzzy import fuzz, process
from typing import Dict, List, Tuple


def fuzzy_search(query: str, choices: Dict[str, List[str]]
                 ) -> List[Tuple[int, str, List[str]]]:
    """ Fuzzy searches through all playlists looking for `query`

        Args:
            query:    search term
            choices:  dict of playlists and tracks:
                        {
                            playlist_id: [
                                'Track 1 - Artists - Album',
                                'Track 2 - Artists - Album'
                            ]
                        }

        Returns:
            List of tuples (matching score, playlist_id)

    """
    results = process.extractBests(
        query, choices=choices, scorer=fuzz.token_set_ratio,
        score_cutoff=90, limit=None
    )
    return [
        (score, playlist_id, data) for (data, score, playlist_id) in results
    ]
