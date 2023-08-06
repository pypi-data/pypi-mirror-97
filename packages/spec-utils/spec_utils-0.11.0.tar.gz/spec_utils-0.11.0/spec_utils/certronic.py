from urllib.parse import urlparse, urlencode, urljoin
from base64 import b64encode, b64decode
import requests
import datetime as dt
# import re
# import math

#__certronic__ = "5.0.0r17013"

class Client:

    def __init__(self, url: str, apikey: str, *args, **kwargs):
        """
        Create a conection with Certronic API using recived parameters.
        """

        self.client_url = urlparse(url)
        self.apikey = b64encode(apikey.encode('utf-8'))


    def __str__(self):
        return f'Client for {self.client_url.geturl()}'

    def __repr__(self):
        return "{}(url='{}', apikey='{}')".format(
            self.__class__.__name__,
            self.client_url.geturl(),
            b64decode(self.apikey).decode('utf-8'),
        )

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        return

    @property
    def headers(self):
        """ Get headers of the client with current data """

        # empty headers initial
        data = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip,deflate",
            "API-Key": b64decode(self.apikey).decode('utf-8')
        }

        return data

    def get(self, path: str, params: dict = None, **kwargs):
        """
        Sends a GET request to Certronic url.

        :param path: path to add to URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`dict` object
        :rtype: dict
        """

        # query prepare
        query = {
            "url": urljoin(self.client_url.geturl(), path),
            "params": params,
            "headers": self.headers,
            "timeout": kwargs.get("timeout", 20),
            "stream": kwargs.get("stream", False)
        }

        # consulting nettime
        response = requests.get(**query)

        # raise if was an error
        if response.status_code not in range(200, 300):
            raise ConnectionError(f'{response.status_code}: {response.text}')

        # to json -> json
        try:
            # if request is stream type, return all response
            if kwargs.get("stream"):
                return response

            # return json response
            return response.json()
        except:
            return {}

    def post(self, path, params: dict = None, data: dict = None,
             json: dict = None, **kwargs):
        """
        Sends a POST request to Certronic url.

        :param url: URL for the new :class:`Request` object.
        :param json: (optional) json data to send in the query of the request 
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the 
            :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`dict` object
        :rtype: dict
        """

        # query prepare
        query = {
            "url": urljoin(self.client_url.geturl(), path),
            "params": params,
            "data": data,
            "json": json,
            "headers": self.headers,
            "timeout": kwargs.get("timeout", 20),
        }

        # consulting nettime
        response = requests.post(**query)

        # raise if was an error
        if response.status_code not in range(200, 300):
            raise ConnectionError(response.text)

        # to json -> json
        try:
            return response.json()
        except:
            return {}

    def get_employees(self, page: int = 1, pageSize: int = 50, \
            updatedFrom: dt.datetime = None, includeDocuments: bool = False, \
            customFields: list = [], **kwargs):
        """
        Get employees from Certronic API with self.get().

        :param updatedFrom: Datetime to apply as start filter of employees 

        :param includeDocuments: True or False to get documents detail
        :param employeeDetail: True to get serialized employee. Code by default
        :param customFields: List of Custom fields to get from employee
        :param pageSize: Max results per page
        :param page: Page number
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """

        # path prepare
        path = f'/employees'

        # datetime to str
        if isinstance(updatedFrom, dt.datetime):
            updatedFrom = updatedFrom.strftime("%Y%m%d%H%M%S")

        # parameters prepare
        params = {
            "updatedFrom": updatedFrom,
            "fromHistory": fromHistory,
            "includeDocuments": includeDocuments,
            "customFields": customFields,
            "pageSize": pageSize,
            "page": page
        }

        # request.get -> json
        return self.get(path=path, params=params, **kwargs)


    def post_clockings(self, clockings: list, **kwargs):
        """
        Send clockings to Certronic API.

        :param clockings: List of clockings. Must be structure like:
            clockings = [{
                "id": 3456,
                "center": "BA01",
                "ss": "12-12345678-9",
                "action": "Entrance",
                "datetime": "2020-02-11T12:39:00.000Z"
            }]
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """

        # path prepare
        path = f'/clockings'

        # 1 dict employee by default
        return self.post(path=path, json=clockings, **kwargs)

