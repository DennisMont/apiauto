"""
(c) Copyright Jalasoft. 2023
"""
import requests
import logging

from config.config import TOKEN_TODO
from utils.singleton import Singleton
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.INFO)


class RestClient(metaclass=Singleton):
    """
    class RestClient
    """

    def send_request(self, method_name, session=None, url="", headers="", data=None):
        methods = {
            "get": session.get,
            "post": session.post,
            "delete": session.delete
        }

        if method_name not in methods:
            raise AssertionError("Invalid method name")

        LOGGER.info("Method name: %s", method_name)
        LOGGER.info("Endpoint (url): %s", url)
        try:
            response = methods[method_name](url, headers=headers, data=data)
            response.raise_for_status()
            LOGGER.info("Status code: %s", response.status_code)
            if hasattr(response, "request"):
                LOGGER.debug("Request: %s", response.request.headers)
            LOGGER.info("Response: %s", response.text.encode("utf-8"))
        except requests.exceptions.HTTPError as http_error:
            LOGGER.error("HTTP error: %s", http_error)
        except requests.exceptions.RequestException as request_error:
            LOGGER.error("Request error: %s", request_error)
        return response

    def get(self, session, url_base, headers):
        """

        :param url_base:
        :param headers:
        :return:
        """
        return self.send_request("get", session, url_base, headers=headers)

    def post(self, session, url_base, headers, data):
        """

        :param url_base:
        :param headers:
        :return:
        """
        return self.send_request("post", session, url_base, headers, data=data)

    def delete(self, session, url_base, headers):
        """

        :param url_base:
        :param headers:
        :return:
        """
        return self.send_request("delete", session, url_base, headers)


if __name__ == "__main__":
    rest_client = RestClient()

    token = TOKEN_TODO

    headers = {
        "Authorization": f"Bearer {token}"
    }

    rest_client.send_request("get", session=requests.session(),
                             url="https://api.todoist.com/rest/v2/projects",
                             headers=headers)
