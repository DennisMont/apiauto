#Arrange, Act, Assertion, Cleanup

#pytest .\tests\test_projects.py -s
#pytest .\tests\test_projects.py -s -m DeleteProjectTDI (Para correr marcas)

import requests
import pytest


class TestProjects:
    def setup_class(self):
        # Constructor setup_class para clases pytest.
        # Arrange
        self.token = "f64f6222098b9848759ff62101776f3d98aa3936"

        self.headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        self.url_base = "https://api.todoist.com/rest/v2/projects"


    def test_get_all_projects(self):
        #Act
        response = requests.get(self.url_base, headers=self.headers)
        print(response.json())
        #Assertion
        assert response.status_code == 200

    def test_create_project(self):

        body_project = {
            "name": "Project Created fro API"
        }

        response = requests.post(self.url_base, headers=self.headers, data=body_project)
        print(response.json())
        assert response.status_code == 200

    @pytest.fixture
    def created_project_id(self):
        body_project = {
            "name": "Project Created to Delete"
        }
        response = requests.post(self.url_base, headers=self.headers, data=body_project)
        project_id = response.json()['id']
        print(project_id)
        print(response.json()['name'])
        assert response.status_code == 200
        return project_id

    def test_get_project(self):
        # Act
        response = requests.get(self.url_base + "/2321090026", headers=self.headers)
        print(response.json())
        # Assertion
        assert response.status_code == 200

    @pytest.mark.UpdateTest
    @pytest.mark.parametrize("name", ["First parametrized update", "Second parametrized update", "Third parametrized update"])
    def test_update_project(self, name):
        # Act
        body_project = {
            "name": name
        }
        response = requests.post(self.url_base + "/2321090026", headers=self.headers, data=body_project)
        print(response.json())
        # Assertion
        assert response.status_code == 200

    @pytest.mark.DeleteProjectTDI
    def test_delete_project(self, created_project_id):
        response = requests.delete(self.url_base + "/" + created_project_id, headers=self.headers)
        # Assertion
        assert response.status_code == 204

    def teardown_class(self):
        print("Teardown class")
