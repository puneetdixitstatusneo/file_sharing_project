from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from main.modules.projects.controller import ProjectsController
from main.modules.projects.schema_validator import AddProjectSchema, UpdateProjectSchema, AssignUsers
from main.modules.auth.controller import AuthUserController
from main.utils import get_data_from_request_or_raise_validation_error


class ProjectListApi(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        """
        This function is used to get the list of projects.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = ProjectsController.get_projects(auth_user)
        return jsonify(response)

    def post(self):
        """
        This function is used to add new project to the database.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(AddProjectSchema, request.json)
        data.update({"user_id": auth_user.id})
        project_id = ProjectsController.add_project(data)
        response = make_response(
            jsonify({"message": "Project added", "location": f"/projects/{project_id}", "id": project_id}), 201
        )
        response.headers["Location"] = f"/projects/{project_id}"
        return response


class ProjectDetailApi(Resource):
    method_decorators = [jwt_required()]

    @staticmethod
    def get(project_id: int):
        """
        This function is used to get the particular project by project_id
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = ProjectsController.get_project_by_project_id(project_id, auth_user)
        return jsonify(response)

    @staticmethod
    def put(project_id: int):
        """
        This function is used to update the project by project_id
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(UpdateProjectSchema, request.json)
        response = ProjectsController.update_project(project_id, data, auth_user)
        return jsonify(response)

    @staticmethod
    def delete(project_id: int):
        """
        This function is used to delete the project by project_id.
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = ProjectsController.delete_project(project_id, auth_user)
        return jsonify(response)


class AddUserToProject(Resource):
    method_decorators = [jwt_required()]

    def post(self, project_id: int):
        data = get_data_from_request_or_raise_validation_error(AssignUsers, request.json)
        response = ProjectsController.add_users_to_project(project_id, data["users_email"])
        return jsonify(response)


project_namespace = Namespace("projects", description="Projects Operations")
project_namespace.add_resource(ProjectListApi, "")
project_namespace.add_resource(ProjectDetailApi, "/<int:project_id>")
project_namespace.add_resource(AddUserToProject, "/<int:project_id>/assign")
