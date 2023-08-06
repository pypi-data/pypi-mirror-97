from urllib.parse import urlparse, urlencode, urljoin
from base64 import b64encode, b64decode
import requests
import datetime
# import re
# import math

__specmanager__ = "5.0.0r17013"

class Client:

    class Authentication:
        def __init__(self, **kwargs):
            self.access_token = kwargs.get('access_token')
            self.token_type = kwargs.get('token_type', 'Bearer').capitalize()
            self.expires = self.get_expires(kwargs.get('expires_in'))

        def __str__(self):
            return f'{self.token_type} {self.access_token}'

        def __bool__(self):
            return self.is_alive

        def get_expires(self, expires_in: int) -> datetime.datetime:
            now = datetime.datetime.now()
            return now + datetime.timedelta(seconds=expires_in - 10)

        @property
        def is_alive(self):
            return self.expires > datetime.datetime.now()

        @property
        def is_expired(self):
            return not self.is_alive

    def __init__(self, url: str, username: str = "Admin", pwd: str = "spec", \
            *args, **kwargs):
        """
        Create a conection with SPEC Manager API using recived parameters.
        """

        # TODO: Implement this

        self.client_url = urlparse(url)
        self.username = username
        self.pwd = b64encode(pwd.encode('utf-8'))

        self.authentication = None

        # connect client and set authentication object automatically
        self.connect()

    def __str__(self):
        return '{} connected to {}'.format(
            self.username,
            self.client_url.geturl()
        )

    def __repr__(self):
        return "{}(url='{}', username='{}', pwd='{}')".format(
            self.__class__.__name__,
            self.client_url.geturl(),
            self.username,
            b64decode(self.pwd).decode('utf-8'),
        )

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        return self.disconnect()
        
    @property
    def headers(self):
        """ Get headers of the client with current data """

        # TODO: Add access_token when is implemented

        # empty headers initial
        data = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip,deflate",
        }

        # logged user
        # if self.authentication:
        #     data["Authorization"] = str(self.authentication)

        return data

    @property
    def is_connected(self):
        """ Informs if client has headers and access_token. """

        return bool(self.authentication)

    @property
    def session_expired(self):
        """
        Informs if the session has expired and it is necessary to reconnect.
        """
        # TODO: Implement this

        # return getattr(self.authentication, 'is_expired', None)
        return False

    def get(self, path: str, params: dict = None, **kwargs):
        """
        Sends a GET request to SPEC Manager url.

        :param path: path to add to URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`dict` object
        :rtype: dict
        """

        # check if session has expired
        if self.session_expired:
            self.reconnect()

        # safety only
        if not self.is_connected and not kwargs.get('force', None):
            raise ConnectionError("Cliente desconectado. Utilice connect().")

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

    def post(self, path, params: dict = None, data: dict = None, \
            json: dict = None, **kwargs):
        """
        Sends a POST request to SPEC Manager url.

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

        # check if session has expired
        if self.session_expired:
            self.reconnect()

        # wait active conection
        if not self.is_connected and not kwargs.get('force', None):
            raise ConnectionError("Cliente desconectado. Utilice connect().")

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

    def connect(self):
        """ Connect the client to get access_token and headers values. """
        # TODO: Implement in SPEC Manager API

        self.authentication = True

    def disconnect(self):
        """ Disconnect the client if is connected. """
        # TODO: Implement in SPEC Manager API

        self.authentication = False

    def reconnect(self):
        """ Reconnect client cleaning headers and access_token. """
        # TODO: Implement in SPEC Manager API

        self.authentication = True

    def get_clockings(self, _type: str, _from: datetime.datetime, \
            _to: datetime.datetime, fromHistory: bool = False, \
            employeeDetail: bool = False, employeeData: list = [], \
            pageSize: int = 20, page: int = 1, **kwargs):
        """
        Get clockings from SM API with self.get() passing _type and 
        parameters recived.

        :param _type: Employee type. Eg. 'employee', 'contractor', etc.
        :param _from: Datetime to apply as start filter of clockings 
        :param _to: Datetime to apply as end filter of clockings 
        :param fromHistory: True or False to get clockings from HISTORICO
        :param employeeDetail: True to get serialized employee. Code by default
        :param employeeData: List of Optional Data of employee to get from SM
        :param pageSize: Max results per page
        :param page: Page number
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """
        
        # path prepare
        path = f'clockings/{_type}'

        # datetime to str
        if isinstance(_from, datetime.datetime):
            _from = _from.strftime("%Y%m%d%H%M%S")

        if isinstance(_to, datetime.datetime):
            _to = _to.strftime("%Y%m%d%H%M%S")

        # parameters prepare
        params = {
            "from": _from,
            "to": _to,
            "fromHistory": fromHistory,
            "employeeDetail": employeeDetail,
            "pageSize": pageSize,
            "page": page
        }

        # append data
        if employeeData:
            params["employeeData"] = ','.join([str(e) for e in employeeData])

        # request.get -> json
        return self.get(path=path, params=params, **kwargs)
        

    def get_clockings_contractor(self, _from: datetime.datetime, \
            _to: datetime.datetime, fromHistory: bool = False, \
            employeeDetail: bool = False, employeeData: list = [], \
            pageSize: int = 20, page: int = 1, **kwargs):
        """
        Get contractor clockings from SM API with self.get_clockings() and 
        recived parameters.

        :param _from: Datetime to apply as start filter of clockings 
        :param _to: Datetime to apply as end filter of clockings 
        :param fromHistory: True or False to get clockings from HISTORICO
        :param employeeDetail: True to get serialized employee. Code by default
        :param employeeData: List of Optional Data of employee to get from SM
        :param pageSize: Max results per page
        :param page: Page number
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """

        # parameters prepare
        params = {
            "_type": "contractor",
            "_from": _from,
            "_to": _to,
            "fromHistory": fromHistory,
            "employeeDetail": employeeDetail,
            "pageSize": pageSize,
            "page": page,
            "employeeData": employeeData
        }

        # request.get -> json
        return self.get_clockings(**params, **kwargs)

    def post_employee(self, _type: str, code: int, nif: str, ss: str, \
            lastName: str, firstName: str, companyCode: str, \
            companyName: str, centers: list = [], **kwargs):
        """
        Send employee to SM API with self.post() passing _type and 
        recived parameters.

        :param _type: str with employee type (enpoint to add in 
            POST /employees/{_type} SM API). E.g.
            'contractor', 'encae', 'employee', etc
        :param code: int with employee code
        :param nif: str with employee DNI field
        :param ss: str with employee SS field
        :param lastName: str with employee lastName field
        :param firstName: str with employee firstName field
        :param companyCode: str with company code (nif)
        :param companyName: str with company name
        :param centers: list of dict with 'center' and 'dueDate' keys. E.g.
            [{
                "center": "AR",
                "dueDate": datetime.date(2020, 12, 31)
            }, {
                "center": "ES",
                "dueDate": datetime.date(2021, 12, 31)
            }]
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """

        # path prepare
        path = f'employees/{_type}'

        # json prepare
        params = {
            "code": code,
            "nif": nif,
            "ss": ss,
            "lastName": lastName,
            "firstName": firstName,
            "companyCode": companyCode,
            "companyName": companyName,
        }

        # centers parse
        if centers:
            params["centers"] = ','.join([
                f'{_c.get("center")}:{_c.get("dueDate").strftime("%Y%m%d")}' \
                    for _c in centers
            ])

        # request.get -> json
        return self.post(path=path, params=params, **kwargs)

    def post_employees(self, employeeData, **kwargs):
        """
        Send employee to SM API with self.post_employee() passing employeeData.

        :param employeeData: Dict or list with params of self.post_employee()
            To get more info of employeeData structure, check help for 
            post_employee() method
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """

        # check items
        if isinstance(employeeData, list):
            # empty response
            response = {}
            
            for employee in employeeData:
                # rewrite if OK, raise if error
                response = self.post_employee(**employee, **kwargs)

            # return last response (or raise before)
            return response

        # 1 dict employee by default
        return self.post_employee(**employeeData, **kwargs)

    def post_employee_encae(self, code: int, nif: str, ss: str, \
            lastName: str, firstName: str, companyCode: str, \
            companyName: str, centers: list = [], **kwargs):
        """
        Send encae employee to SM API with self.post_employee() and 
        recived parameters.

        :param code: int with employee code
        :param nif: str with employee DNI field
        :param ss: str with employee SS field
        :param lastName: str with employee lastName field
        :param firstName: str with employee firstName field
        :param companyCode: str with company code (nif)
        :param companyName: str with company name
        :param centers: list of dict with 'center' and 'dueDate' keys. E.g.
            [{
                "center": "AR",
                "dueDate": datetime.date(2020, 12, 31)
            }, {
                "center": "ES",
                "dueDate": datetime.date(2021, 12, 31)
            }]
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """

        # json prepare
        query = {
            "_type": "encae",
            "code": code,
            "nif": nif,
            "ss": ss,
            "lastName": lastName,
            "firstName": firstName,
            "companyCode": companyCode,
            "companyName": companyName,
            "centers": centers
        }

        # request.get -> json
        return self.post_employee(**query, **kwargs)

