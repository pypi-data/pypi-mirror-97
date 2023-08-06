from constants import key
from datetime import datetime
import requests
from io import BytesIO


class Earth:
    def __init__(self, inlat: float, inlon: float, indate: str = str(datetime.now().date()), indim: float = .025):
        """
        This endpoint retrieves the date-times and asset names for closest available imagery for a supplied location and date.


        :param inlat: Latitude
        :param inlon: Longitude
        :param indate: beginning of 30 day date range that will be used to look for closest image to that date
        :param indim: width and height of image in degrees
        """
        indate = str(datetime.strptime(indate, "%Y-%m-%d").date())
        payload = {'api_key': key, 'lat': inlat, 'lon': inlon, "date": indate, "dim": indim}
        response = requests.get(f'https://api.nasa.gov/planetary/earth/assets?', params=payload)
        self.limit = response.headers['X-RateLimit-Limit']
        self.remaining = response.headers['X-RateLimit-Remaining']
        response = response.json()
        if 'msg' in response:
            raise ValueError(response['msg'])
        self.date = response['date']
        self.id = response['id']
        self.dataset = response['resource']['dataset']
        self.planet = response['resource']['planet']
        self.url = response['url']
        self.bytesimage = BytesIO(requests.get(self.url).content)
