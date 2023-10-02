import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.INFO)

class Comments(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """

        :return:
        """
        cls.url_comments = "https://api.todoist.com/rest/v2/comments"
        cls.session = requests.Session()
        cls.task_id = TodoBase().get_all_tasks().json()[1]["id"]

    def test_get_all_comments(self):
        """

        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        url_get_all_comments = f"{self.url_comments}?task_id={task_id}"
        response = RestClient().send_request("get", session=self.session,
                                             headers=HEADERS, url=url_get_all_comments)
        LOGGER.info("Response to Get All Comments request: %s", response.json())
        assert response.status_code == 200

    def test_create_comment(self):
        """

        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        content_comment = "A new comment is born"
        response = self.create_comment(content_comment, "task_id", task_id)
        assert response.status_code == 200

    def test_get_comment_by_id(self):
        """

        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)

        content_comment = "A new comment is born for Get Comment By Id"
        response = self.create_comment(content_comment, "task_id", task_id)
        comment_id = response.json()["id"]
        LOGGER.info("Comment Id: %s", comment_id)

        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("get", session=self.session,
                                             headers=HEADERS, url=url_comment)
        LOGGER.info("Response to Get Comment By Id request: %s", response.json())
        assert response.status_code == 200

    def test_update_comment(self):
        """

        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)

        content_comment = "A new comment is born to be updated"
        response = self.create_comment(content_comment, "task_id", task_id)
        comment_id = response.json()["id"]
        LOGGER.info("Comment Id: %s", comment_id)

        url_comment = f"{self.url_comments}/{comment_id}"
        data_for_update = {
            "content": "Un request pasó por aquí y me actualizo con su rasho laser"
        }
        response = RestClient().send_request("post", session=self.session,
                                             headers=HEADERS, url=url_comment, data=data_for_update)
        LOGGER.info("Response to Update Comment request: %s", response.json())
        assert response.status_code == 200

    def test_delete_comment(self):
        """

        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)

        content_comment = "No me quiero ir señor Stark!"
        response = self.create_comment(content_comment, "task_id", task_id)
        comment_id = response.json()["id"]
        LOGGER.info("Comment Id: %s", comment_id)

        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("delete", session=self.session,
                                             headers=HEADERS, url=url_comment)
        assert response.status_code == 204

    def create_comment(self, content, type_id, task_or_project_id):
        data = {
            "content": content
        }
        if type_id == "project_id":
            data["project_id"] = task_or_project_id
        elif type_id == "task_id":
            data["task_id"] = task_or_project_id

        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_comments, data=data)

        return response
