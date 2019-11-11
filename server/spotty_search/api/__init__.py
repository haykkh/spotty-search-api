# -*- coding: utf-8 -*-
"""
    spotty_search.api
    ~~~~~~~~~~~~~~~~~

    Base interactions with pyfy Spotify api

    Contains classes for Tracks, Playlist, and User
    Initializes synced pyfy Client
"""

from typing import List, Dict
from pyfy import Spotify, ClientCreds


def catcher(playlist: dict) -> str:
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
    """
    def __init__(self, i: str, n: str, t: List[Track], u: str) -> None:
        self.id = i
        self.name = n
        self.tracks = t
        self.img = u


class User:
    """ Spotify user object

        Attributes:
            spt:                 pyfy sync Spotify client
            number_of_playlists: number of playlist a user has
            playlists:           list of user's Playlists
    """
    def __init__(self, s: Spotify, p: Dict[str, Playlist] = {},
                 n: int = 0) -> None:
        self.spt = s
        self.playlists = p
        self.number_of_playlists = n

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
                self.playlists[playlist['id']] = Playlist(
                    playlist['id'],  # Playlist.id
                    playlist['name'],  # Playlist.name
                    [  # list comp of Tracks being initialised from call to Spotify web api
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
                        in self.spt.playlist_tracks(playlist['id'])['items']  # call to web api
                    ],  # Playlist.tracks
                    catcher(playlist),  # Playlist.img
                )

            i += 1


client = ClientCreds()
spot = User(Spotify())
