from datetime import datetime
from io import BytesIO
from constants import key
import requests


class APOD:
    def __init__(self, indate: str = str(datetime.now().date())):
        """

        :param indate: Date must be between June 16, 1995 and the current date.

        Gives the astronomy image of the day for the date passed in
        NASA's github https://github.com/nasa/apod-api
        """
        indate = datetime.strptime(indate, "%Y-%m-%d").date()
        if not indate >= datetime(1995, 6, 16).date() or not indate <= datetime.now().date():
            raise ValueError("Date must be between June 16, 1995 and the current date.")

        self.date = indate
        payload = {'api_key': key, 'date': str(self.date)}
        response = requests.get(f'https://api.nasa.gov/planetary/apod?', params=payload)
        self.limit = response.headers['X-RateLimit-Limit']
        self.remaining = response.headers['X-RateLimit-Remaining']
        response = response.json()

        self.copyright = response.get('copyright', None)
        self.explanation = response['explanation']
        self.hdurl = response.get('hdurl', None)
        self.media_type = response['media_type']
        self.title = response['title']
        self.url = response['url']
        self.bytesimage = BytesIO(requests.get(self.url).content) if self.media_type != "video" else None
