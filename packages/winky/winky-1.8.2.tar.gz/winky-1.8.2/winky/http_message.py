import requests
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
import os


class HTTPMessage:

    def __init__(self, body=""):
        self.__body = body
        self.__headers = {}
        self.__code = 200
        self.__auth__ = None
        self.__attach = None

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, text):
        self.__body = text

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = headers

    def set_body_from_file(self, path):
        with open(path, 'r') as file:
            self.__body = file.read()

    @property
    def auth(self):
        class auth:
            @staticmethod
            def digest(login, password):
                self.__auth__ = HTTPDigestAuth(login, password)

            @staticmethod
            def basic(login, password):
                self.__auth__ = HTTPBasicAuth(login, password)

        return auth

    def attach(self, *files):
        self.__attach = {}
        for file in files:
            if type(file) is list:
                self.__attach[file[0]] = open(file[1], 'rb')
            else:
                self.__attach[os.path.basename(file)] = open(file, 'rb')

    def post(self, url, port, metod="/", timeout=10):
        endpoint = f"{url}:{port}{metod}"
        response = requests.post(endpoint,
                                 headers=self.__headers,
                                 data=self.__body.encode(),
                                 timeout=timeout,
                                 verify=False,
                                 auth=self.__auth__,
                                 files=self.__attach)
        return self.__make_response_message(response)

    def put(self, url, port, metod="/", timeout=10):
        endpoint = f"{url}:{port}{metod}"
        response = requests.put(endpoint,
                                headers=self.__headers,
                                data=self.__body.encode(),
                                timeout=timeout,
                                verify=False,
                                auth=self.__auth__,
                                files=self.__attach)
        return self.__make_response_message(response)

    def patch(self, url, port, metod="/", timeout=10):
        endpoint = f"{url}:{port}{metod}"
        response = requests.patch(endpoint,
                                  headers=self.__headers,
                                  data=self.__body.encode(),
                                  timeout=timeout,
                                  verify=False,
                                  auth=self.__auth__,
                                  files=self.__attach)
        return self.__make_response_message(response)

    def delete(self, url, port, metod="/", timeout=10):
        endpoint = f"{url}:{port}{metod}"
        response = requests.delete(endpoint,
                                   headers=self.__headers,
                                   data=self.__body.encode(),
                                   timeout=timeout,
                                   verify=False,
                                   auth=self.__auth__,
                                   files=self.__attach)
        return self.__make_response_message(response)

    def get(self, url, port, metod="/", timeout=10):
        endpoint = f"{url}:{port}{metod}"
        response = requests.get(endpoint,
                                headers=self.__headers,
                                timeout=timeout,
                                verify=False,
                                auth=self.__auth__)
        return self.__make_response_message(response)

    @staticmethod
    def __make_response_message(response):
        response_message = HTTPMessage(response.text)
        response_message.headers = response.headers
        response_message.__code = response.status_code
        return response_message
