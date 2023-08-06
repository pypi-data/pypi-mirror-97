# coding=utf-8
"""
作者：vissy@zhu
"""

import requests
from testdata import http


class ConfigHttp:

    def __init__(self):
        global scheme, api_url, www_url, web_url, port
        scheme = http.data["scheme"]
        api_url = http.data["api_url"]
        www_url = http.data["www_url"]
        web_url = http.data["web_url"]
        port = http.data["port"]
        self.headers = {}
        # self.params = {}
        self.data = {}
        self.url = {}
        # self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = scheme + '://' + api_url + url

    def set_www_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = scheme + '://' + www_url + url

    def set_web_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = scheme + '://' + web_url + url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.__data = data

    # defined http_data.py get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http_data.py post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.__url,  headers=self.headers,json=self.__data)
            # response.raise_for_status()
            return response
        except TimeoutError:
            return None
