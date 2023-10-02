"""
(c) Copyright Jalasoft. 2023
"""
import logging
import unittest
import requests
from nose2.tools import params

from config.config import TOKEN_TODO
from utils.logger import get_logger

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

        cls.headers = {
            "Authorization": "Bearer {}".format(cls.token)
        }
        cls.url_base = "https://api.todoist.com/rest/v2/projects"
        body_project = {
            "name": "Delete me"
        }
        response = requests.post(cls.url_base, headers=cls.headers, data=body_project)
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
        response = requests.get(self.url_base, headers=self.headers)
        print(response.json())
        assert response.status_code == 200

    def test_2_create_project(self):
        """
        body_project = {
            "name": "Project Created from API"
        }
        response = requests.post(self.url_base, headers=self.headers, data=body_project)
        print(response.json())
        assert response.status_code == 200
        """

    def test_3_get_project_id(self):
        """

        :return:
        """
        response = requests.get(f"{self.url_base}/{self.project_id}", headers=self.headers)
        print(response.json())
        LOGGER.info("Response for create project: %s", response.json())
        # Assertion
        assert response.status_code == 200

    def test_4_delete_project_id(self):
        """

        :return:
        """
        response = requests.delete(f"{self.url_base}/{self.project_id}", headers=self.headers)
        # Assertion
        assert response.status_code == 204


    @params("First update with nose2", "Second update with nose2", "Third update with nose2")
    def test_5_update_project_id(self, name):
        """

        :param name:
        :return:
        """
        print(name)
        body_project = {
            "name": name
        }
        response = requests.post(f"{self.url_base}/{self.project_id}",
                                 headers=self.headers, data=body_project)
        self.project_name = response.json()['name']
        print(self.project_name)
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
        response = requests.delete(f"{cls.url_base}/{cls.project_id}", headers=cls.headers)
        print(f"Response: {response.status_code}")
