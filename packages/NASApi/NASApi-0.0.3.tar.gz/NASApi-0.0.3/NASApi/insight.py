from constants import key
from typing import NamedTuple
from datetime import datetime
import requests


class Insight:
    def __init__(self):
        """
        Provides per-Sol summary data for each of the last seven available Sols
        NASA's documentation https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf

        """
        payload = {'api_key': key, 'feedtype': "json", 'ver': "1.0"}
        response = requests.get(f'https://api.nasa.gov/insight_weather/?', params=payload)
        self.limit = response.headers['X-RateLimit-Limit']
        self.remaining = response.headers['X-RateLimit-Remaining']
        response = response.json()
        self.solkeys = response['sol_keys']
        self.atmotemp, self.horzonws, self.atmopres, self.utcs, self.seasons = [], [], [], [], []
        for solk in self.solkeys:
            self.atmotemp.append(AtmoTemp._make(response[solk]['AT'].values()))
            self.horzonws.append(HorzonWS._make(response[solk]['HWS'].values()))
            self.atmopres.append(AtmoPres._make(response[solk]['PRE'].values()))
            self.utcs.append(FirstLastUTC._make([response[solk]['First_UTC'], response[solk]['Last_UTC']]))
            self.seasons.append(response[solk]['Season'])


class AtmoTemp(NamedTuple):
    average: float
    count: int
    minimum: float
    maximum: float


class HorzonWS(NamedTuple):
    average: float
    count: int
    minimum: float
    maximum: float


class AtmoPres(NamedTuple):
    average: float
    count: int
    minimum: float
    maximum: float


class FirstLastUTC(NamedTuple):
    first: datetime
    last: datetime
