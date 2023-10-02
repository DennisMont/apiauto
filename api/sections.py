import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.session = requests.Session()

        cls.project_id = TodoBase().get_all_projects().json()[1]["id"]

    def test_create_session(self):
        """
        Test to create session
        :return:
        """
        data = {
            "project_id": self.project_id,
            "name": "Section 2"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_section, data=data)
        assert response.status_code == 200

    def test_get_all_sections(self):

        response = TodoBase().get_all_sections()
        LOGGER.info("Number of sections returned: %s", len(response.json()))
        assert response.status_code == 200

    def test_get_all_sections_by_project(self):
        if self.project_id:
            url_section = f"{self.url_section}?project_id={self.project_id}"

        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        LOGGER.info("Number of sections returned: %s", len(response.json()))
        assert response.status_code == 200

    def test_get_section(self):
        response = TodoBase().get_all_sections()
        section_id = response.json()[0]["id"]
        section_name = response.json()[0]["name"]
        LOGGER.info("Section Id: %s", section_id)
        LOGGER.info("Section Name: %s", section_name)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        assert response.status_code == 200

    def test_update_section(self):
        """
        - Get last project
        - Create a session in the project
        - UPDATE THE CREATED SESSION
        :return:
        """

        #Get last project
        projects = TodoBase().get_all_projects()
        last_project_id = projects.json()[-1]["id"]
        last_project_name = projects.json()[-1]["name"]
        LOGGER.info("last project Id: %s", last_project_id)
        LOGGER.info("last project Name: %s", last_project_name)

        #Create a section in last project
        data = {
            "project_id": last_project_id,
            "name": "Section Created from API"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_section, data=data)
        section_id = response.json()["id"]
        LOGGER.info("Section Id: %s", section_id)

        #Update the created section
        data_to_update = {
            "name": "Section Updated from API"
        }
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_section, data=data_to_update)
        assert response.status_code == 200

    def test_delete_section(self):
        """
        - Get last project
        - Create a session in the project
        - DELETE THE CREATED SESSION
        :return:
        """
        # Get last project
        projects = TodoBase().get_all_projects()
        last_project_id = projects.json()[-1]["id"]
        last_project_name = projects.json()[-1]["name"]
        LOGGER.info("last project Id: %s", last_project_id)
        LOGGER.info("last project Name: %s", last_project_name)

        # Create a section in last project
        data = {
            "project_id": last_project_id,
            "name": "Section Created from API to be deleted"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_section, data=data)
        section_id = response.json()["id"]
        LOGGER.info("Section Id: %s", section_id)

        # Update the created section
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_section)
        assert response.status_code == 204
