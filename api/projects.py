"""
(c) Copyright Jalasoft. 2023
"""
import logging
import unittest
import requests
from nose2.tools import params

from config.config import TOKEN_TODO
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.INFO)


class Projects(unittest.TestCase):
    """
    NOSE2
    """

    @classmethod
    def setUpClass(cls):
        """
        Se ejecuta una sola vez al inicio
        """
        print("Setup class")
        cls.token = TOKEN_TODO

        cls.session = requests.session()
        cls.headers = {
            "Authorization": f"Bearer {cls.token}"
            # "Authorization": "Bearer {}".format(cls.token)
        }
        cls.url_base = "https://api.todoist.com/rest/v2/projects"
        body_project = {
            "name": "Delete me"
        }

        response = RestClient().send_request("post", cls.session,
                                             cls.url_base, headers=cls.headers,
                                             data=body_project)
        print(response.json())
        cls.project_id = response.json()['id']
        cls.project_name = response.json()['name']

    def setUp(self):
        """
            Se ejecuta antes de cada test cada test
        """
        # Constructor setup_class para clases pytest.
        # Arrange
        print("setup")

    def test_1_get_all_projects(self):
        """

        :return:
        """
        # response = requests.get(self.url_base, headers=self.headers, timeout=10)
        response = RestClient().send_request("get", self.session,
                                             self.url_base, headers=self.headers)
        LOGGER.info("Response for get all projects: %s", response.text.encode("utf-8"))
        assert response.status_code == 200

    def test_2_get_project_id(self):
        """

        :return:
        """
        response = RestClient().send_request("get", self.session,
                                             f"{self.url_base}/{self.project_id}",
                                             headers=self.headers)
        print(response.json())
        LOGGER.info("Response for get project: %s", response.text.encode("utf-8"))
        # Assertion
        assert response.status_code == 200

    @params("First update with nose2", "Second update with nose2", "Third update with nose2")
    def To_review_test_3_update_project_id(self, name):
        """

        :param name:
        :return:
        """
        print(name)
        body_project = {
            "name": name
        }
        response = requests.post(f"{self.url_base}/{self.project_id}",
                                 headers=self.headers, data=body_project, timeout=10)
        self.project_name = response.json()['name']
        LOGGER.info("Response for update project: %s", self.project_name)
        assert response.status_code == 200

    def test_4_update_project_id(self):
        """

        :return:
        """
        body_project = {
            "name": "Born to be deleted"
        }
        response = RestClient().send_request("post", self.session,
                                             f"{self.url_base}/{self.project_id}",
                                             headers=self.headers,
                                             data=body_project)
        self.project_name = response.json()['name']
        LOGGER.info("Response for update project: %s", self.project_name)
        assert response.status_code == 200

    def test_5_delete_project_id(self):
        """

        :return:
        """
        response = RestClient().send_request("delete", self.session,
                                             f"{self.url_base}/{self.project_id}",
                                             headers=self.headers)
        # Assertion
        assert response.status_code == 204

    def test_6_create_project(self):
        """

        :return:
        """
        RestClient().send_request("delete", self.session,
                                  f"{self.url_base}/{self.project_id}",
                                  headers=self.headers)

        body_project = {
            "name": "Project Created from API"
        }
        response = RestClient().send_request("post", self.session,
                                             self.url_base, headers=self.headers,
                                             data=body_project)
        LOGGER.info("Response for create project: %s", response.json())
        project_id_created = response.json()['id']
        LOGGER.info("Response for create project: %s", project_id_created)

        RestClient().send_request("delete", self.session,
                                  f"{self.url_base}/{project_id_created}", headers=self.headers)

        assert response.status_code == 200

    def tearDown(self):
        """

        :return:
        """
        print("Tear down")

    @classmethod
    def tearDownClass(cls):
        """

        :return:
        """
        print("Teardown class")
        print(f"Deleting project {cls.project_name} with id {cls.project_id}")
        response = RestClient().send_request("delete", cls.session,
                                             f"{cls.url_base}/{cls.project_id}",
                                             headers=cls.headers)
        print(f"Response: {response.status_code}")
        LOGGER.info("Response for delete project: %s", response.status_code)
