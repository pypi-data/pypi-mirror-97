from collections import namedtuple
from constants import key
from datetime import datetime
from io import BytesIO
import requests


class APOD:
    def __init__(self, indate=str(datetime.now().date()), start_date: str = None, end_date: str = None,
                 count: int = None, thumbs: bool = True):
        """
        Gives the astronomy image of the day for the date passed in
        NASA's github https://github.com/nasa/apod-api

        :param indate: The date of the APOD image to retrieve (Date must be between June 16, 1995 and the current date)
        :param start_date The start of a date range, when requesting date for a range of dates. Cannot be used with date
        :param end_date	The end of the date range, when used with start_date.
        :param count If this is specified then count randomly chosen images will be returned (Cannot be used with date or start_date and end_date)
        :param thumbs Return the URL of video thumbnail (If an APOD is not a video, this parameter is ignored)
        """

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else datetime.strptime(datetime.now().date(), "%Y-%m-%d").date()
            if not datetime.now().date() >= start_date >= datetime(1995, 6, 16).date() or start_date > end_date:
                raise ValueError("start_date must be between June 16, 1995 and the current date and start_date has to be before end_date.")
            elif not datetime.now().date() >= end_date >= datetime(1995, 6, 16).date() or start_date > end_date:
                raise ValueError("start_date must be between June 16, 1995 and the current date and start_date has to be before end_date.")
            payload = {'api_key': key, 'start_date': start_date, 'end_date': end_date, 'thumbs': thumbs}
        elif count:
            if 100 >= count > 0:
                payload = {'api_key': key, 'count': count, 'thumbs': thumbs}
            else:
                raise ValueError("Count cannot exceed 100 and must be positive (0 < count <= 100)")
        else:
            indate = datetime.strptime(indate, "%Y-%m-%d").date()
            if not datetime.now().date() >= indate >= datetime(1995, 6, 16).date():
                raise ValueError("Date must be between June 16, 1995 and the current date.")
            payload = {'api_key': key, 'date': str(indate), 'thumbs': thumbs}

        response = requests.get(f'https://api.nasa.gov/planetary/apod?', params=payload)
        self.limit = response.headers['X-RateLimit-Limit']
        self.remaining = response.headers['X-RateLimit-Remaining']
        response = response.json()
        if start_date or count:
            self.APODitems = []
            for resp in response:
                self.APODitems.append(namedtuple("APODitem", resp.keys())(*resp.values()))
        else:
            self.date = response['date']
            self.copyright = response.get('copyright', None)
            self.explanation = response['explanation']
            self.hdurl = response.get('hdurl', None)
            self.media_type = response['media_type']
            self.title = response['title']
            self.url = response['url']
            self.bytes_url = BytesIO(requests.get(self.url).content) if self.media_type != "video" else None
            self.thumbnail_url = response.get('thumbnail_url', None)
            self.bytes_thumbnail = BytesIO(requests.get(self.thumbnail_url).content) if self.media_type == "video" else None

