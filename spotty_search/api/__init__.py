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

    def track_fetcher(self, offset: int, playlist_id: str) -> List[dict]:
        """ Calls pyfy api to fetch a playlist's tracks

            Throttles connection and tries again if Spotify returns 429 error
            (API rate limit exceeded)

            Args:
                user:        pyfy sync Spotify client
                off:         offset for API call
                playlist_id: ID of playlist (duh)

            Returns:
                List of dictionaries containing tracks in playlist
                    [
                        {
                            track: info
                        }
                    ]

        """
        try:
            return self.spt.playlist_tracks(playlist_id,
                                            offset=offset*100)['items']
        except excs.ApiError as e:
            if e.code == 429:
                retry_after = int(e.http_response.headers['Retry-After'])
                print(f'429 ApiError, retrying after {retry_after * 2} seconds')
                sleep(retry_after * 2)
                return self.track_fetcher(offset, playlist_id)

    def track_comprehender(self, tracks: List[dict]) -> List[Track]:
        """ Extracts relevant information from Spotify
            web api return into list of Track objects

            Args:
                tracks: List of dictionaries containing tracks in playlist
                        (return from track_fetcher)

            Returns:
                List of Track objects
        """
        return [
            Track(
                track['track']['id'],             # Track.id
                track['track']['name'],           # Track.name
                [
                    artist['name']
                    for artist
                    in track['track']['artists']
                ],                                # Track.artists
                track['track']['album']['name'],  # Track.album
            )
            for track
            in tracks
        ]

    def track_generator(self, playlist: dict) -> List[Track]:
        """ Fetches all tracks in a playlist

            Spotify web api returns max 100 tracks per query
            so we use a while look to fetch chunks of <=100 tracks

            Args:
                playlist: JSON playlist data straight from Spotify web api

            Returns:
                List of all Tracks in playlist
        """
        tracks = []
        i = 0
        while i * 100 < playlist['tracks']['total']:
            tracks.extend(
                self.track_comprehender(
                    self.track_fetcher(i, playlist['id'])
                ))
            i += 1
        return tracks

    def catcher(self, playlist: dict) -> Optional[str]:
        """ Circumventing weird returns by Spotify
            web api sometimes causing IndexErrors

            Args:
                playlist: JSON playlist data straight from Spotify web api

            Returns:
                URL of playlist cover image or None
        """
        try:
            return playlist['images'][0]['url']
        except IndexError:
            return None

    def add_playlist(self, playlist: dict, tracks: List[Track]) -> None:
        """ Adds a playlist to self.playlists

            Args:
                playlist: JSON playlist data straight from Spotify web api
                tracks:   list of all Tracks in playlist

            Returns:
                None
        """
        self.playlists[playlist['id']] = Playlist(
            playlist['id'],               # Playlist.id
            playlist['name'],             # Playlist.name
            tracks,                       # Playlist.tracks
            playlist['tracks']['total'],  # Playlist.number_of_tracks
            self.catcher(playlist),       # Playlist.img
            f'{request.url_root}/search/playlist/{playlist["id"]}',  # Playlist.uri
        )

    def add_playlist_and_tracks(self, playlist: dict,
                                tracks: List[Track]) -> None:
        """ Adds track name, artists, and album to self.playlists_and_tracks
            with playlist id as key

            Args:
                playlist: JSON playlist data straight from Spotify web api
                tracks:   list of all Tracks in playlist

            Returns:
                None
        """
        self.playlists_and_tracks[playlist['id']] = [
            f'{track.name} - {", ".join(track.artists)} - {track.album}'
            for track in tracks
        ]

    def initdata(self) -> None:
        """ Initializes a user's playlist data after authentication

            Spotify web api returns max 50 items (playlists) per query
            so we use a while loop to fetch chunks of <=50 items

            Returns:
                None
        """
        # get total number of playlists followed by user
        self.number_of_playlists = self.spt.user_playlists()['total']

        i = 0
        while i * 50 < self.number_of_playlists:
            for playlist in self.spt.user_playlists(spot.spt.user_creds.id,
                                                    50, i * 50)['items']:

                tracks = self.track_generator(playlist)
                self.add_playlist(playlist, tracks)
                self.add_playlist_and_tracks(playlist, tracks)

            i += 1


client = ClientCreds()
spot = User(Spotify())
