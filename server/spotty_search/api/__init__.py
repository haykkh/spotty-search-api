# -*- coding: utf-8 -*-
"""
    spotty_search.api
    ~~~~~~~~~~~~~~~~~

    Base interactions with pyfy Spotify api

    Contains classes for Tracks, Playlist, and User
    Initializes synced pyfy Client
"""

from typing import List, Dict, Optional
from pyfy import Spotify, ClientCreds, excs
from flask import request
from time import sleep


def catcher(playlist: dict) -> Optional[str]:
    """ Circumventing weird returns by Spotify
        web api sometimes causing IndexErrors

        Args:
            playlist: dict containing Spotify web api
                      return for specific playlist

        Returns:
            URL of playlist cover image or None
    """
    try:
        return playlist['images'][0]['url']
    except IndexError:
        return None


class Track:
    """ Spotify track object

        Attributes:
            id:      Spotify ID of track
            name:    name of track
            artists: list of artists
            album:   album of track
    """
    def __init__(self, i: str, n: str, ar: List[str], al: str) -> None:
        self.id = i
        self.name = n
        self.artists = ar
        self.album = al


class Playlist:
    """ Spotify playlist object

        Attributes:
            id:     Spotify ID of playlist
            name:   name of playlist
            tracks: list of Tracks
            img:    url of playlist cover image
            uri:    REST return uri of playlist
    """
    def __init__(self, i: str, n: str, t: List[Track],
                 nt: int, im: Optional[str], u: str) -> None:
        self.id = i
        self.name = n
        self.tracks = t
        self.number_of_tracks = nt
        self.img = im
        self.uri = u
        self.tracks_uri = f'{u}/tracks'


class User:
    """ Spotify user object

        Attributes:
            spt:                 pyfy sync Spotify client
            playlists:           list of user's Playlists
            number_of_playlists: number of playlist a user has
    """
    def __init__(self, s: Spotify, p: Dict[str, Playlist] = {},
                 n: int = 0, pt: Optional[Dict[str, List[str]]] = {}) -> None:
        self.spt = s
        self.playlists = p
        self.number_of_playlists = n
        self.playlists_and_tracks = pt

    def initdata(self) -> None:
        """ Initializes a user's playlist data after authentication

            Spotify web api returns max 50 items (playlists) per query
            so we use a while loop to fetch chunks of <=50 items
        """

        # get total number of playlists followed by user
        self.number_of_playlists = self.spt.user_playlists()['total']

        i = 0
        while i * 50 < self.number_of_playlists:
            for playlist in self.spt.user_playlists(spot.spt.user_creds.id, 50, i * 50)['items']:
                # adds Playlist to dictionary with its ID as the key
                tracks = []
                j = 0
                while j * 100 < playlist['tracks']['total']:

                    try:
                        trcks = self.spt.playlist_tracks(playlist['id'], offset=j*100)['items']
                    except excs.ApiError as e:
                        if e.code == 429:
                            time = int(e.http_response.headers['Retry-After'])
                            print(f'ERROR ERROR\n\n\n\nERROR ERROR\n\n\nsleeping {time} seconds')
                            sleep(time * 2)
                            trcks = self.spt.playlist_tracks(playlist['id'], offset=j*100)['items']

                    batch = [  # list comp of Tracks being initialised from call to Spotify web api
                        Track(
                            track['track']['id'],  # Track.id
                            track['track']['name'],   # Track.name
                            [
                                artist['name']
                                for artist
                                in track['track']['artists']
                            ],  # Track.artists
                            track['track']['album']['name'],  # Track.album
                            )
                        for track
                        in trcks
                    ]
                    tracks.extend(batch)

                    j += 1

                self.playlists[playlist['id']] = Playlist(
                    playlist['id'],  # Playlist.id
                    playlist['name'],  # Playlist.name
                    tracks,  # Playlist.tracks
                    playlist['tracks']['total'],  # Playlist.number_of_tracks
                    catcher(playlist),  # Playlist.img
                    f'{request.url_root}search/playlist/{playlist["id"]}',  # Playlist.uri
                )

                self.playlists_and_tracks[playlist['id']] = [
                    f'{track.name} - {", ".join(track.artists)} - {track.album}'
                    for track in self.playlists[playlist['id']].tracks
                ]

            i += 1


client = ClientCreds()
spot = User(Spotify())
