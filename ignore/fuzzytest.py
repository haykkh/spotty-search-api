import json
from fuzzywuzzy import fuzz, process



with open('playlistsandtracks.json') as f:
    data = json.load(f)

def search(x, scorer):
    results = process.extractBests(
        x, choices=data, scorer=scorer, score_cutoff=90, limit=None
    )
    return [
        (score, playlist_id) for (data, score, playlist_id) in results
    ]


def ratio(x):
    print("ratio")
    print(search(x, fuzz.ratio))

def partial_ratio(x):
    print("partial_ratio")
    print(search(x, fuzz.partial_ratio))

def token_sort(x):
    print("token_sort")
    print(search(x, fuzz.token_sort_ratio))

def token_set(x):
    print("token_set")
    print(search(x, fuzz.token_set_ratio))

def partial_token_sort(x):
    print("partial_token_sort")
    print(search(x, fuzz.partial_token_sort_ratio))

def partial_token_set(x):
    print("partial_token_set")
    print(search(x, fuzz.partial_token_set_ratio))


def mega(x):
    #ratio(x)
    #partial_ratio(x)
    token_set(x)
    token_sort(x)
    partial_token_set(x)
    partial_token_sort(x)