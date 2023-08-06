from datetime import datetime
from io import BytesIO
from constants import key
from typing import NamedTuple
import requests

geon = "natural"
gada = ""


class EPIC:
    def __init__(self, eon: str = "natural", ada: str = ""):
        """
        Provides information on the daily imagery collected by DSCOVR's Earth Polychromatic Imaging Camera
        NASA's documentation: https://epic.gsfc.nasa.gov/about/api

        :param eon: enhanced or natural
        :param ada: all, date, or available
        """
        global geon
        global gada
        eon, ada = eon.lower(), ada.lower()
        payload = {'api_key': key}
        url = f"https://api.nasa.gov/EPIC/api/{eon}/"
        try:
            ada = datetime.strptime(ada, "%Y-%m-%d").date()
            url = url + "date/" + str(ada) + "?"
        except ValueError:
            url = url + f'{ada}?'
        geon = eon
        gada = ada
        response = requests.get(url, params=payload)
        self.limit = response.headers['X-RateLimit-Limit']
        self.remaining = response.headers['X-RateLimit-Remaining']
        response = response.json()

        self.dates = []
        if ada == "available":
            for r in response:
                self.dates.append(r)
        elif ada == "all":
            for r in response:
                self.dates.append(r['date'])
        else:
            self.identifiers, self.captions, self.images, self.versions = [], [], [], []
            self.centroidcords, self.dscovrpos, self.lunarpos, self.sunpos, self.attquarts = [], [], [], [], []
            for r in response:
                self.identifiers.append(r['identifier'])
                self.captions.append(r['caption'])
                self.images.append(r['image'])
                self.versions.append(r['version'])
                self.centroidcords.append(CentroidCoords._make(r['centroid_coordinates'].values()))
                self.dscovrpos.append(DscovrPos._make(r['dscovr_j2000_position'].values()))
                self.lunarpos.append(LunarPos._make(r['lunar_j2000_position'].values()))
                self.sunpos.append(SunPos._make(r['sun_j2000_position'].values()))
                self.attquarts.append(AttitudeQuaternions._make(r['attitude_quaternions'].values()))
                self.dates.append(r['date'])

    def __str__(self):
        if gada in ["available", "all"]:
            output = f"dates: {self.dates}"
        else:
            output = f"identifiers: {self.identifiers}\ncaptions: {self.captions}\nimages: {self.images}\n"
            output += f"versions: {self.versions}\ncentroid coordinates: {self.centroidcords}\n"
            output += f"dscover position: {self.dscovrpos}\nlunar position: {self.lunarpos}\nsun position {self.sunpos}"
            output += f"\nattitude quaternions: {self.attquarts}\ndates: {self.dates}"
        return output

    @staticmethod
    def getbytesimage(image: str, date: str) -> BytesIO:
        image = requests.get(f"https://api.nasa.gov/EPIC/archive/{geon}/{date[:10].replace('-', '/')}/png/{image}"
                             f".png?api_key={key}")
        return BytesIO(image.content)


class CentroidCoords(NamedTuple):
    latitude: float
    longitude: float


class DscovrPos(NamedTuple):
    x: float
    y: float
    z: float


class LunarPos(NamedTuple):
    x: float
    y: float
    z: float


class SunPos(NamedTuple):
    x: float
    y: float
    z: float


class AttitudeQuaternions(NamedTuple):
    q0: float
    q1: float
    q2: float
    q3: float
