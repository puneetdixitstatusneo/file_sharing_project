from main.custom_exceptions import EntityNotFoundError, UnauthorizedUserError
from main.modules.projects.model import Projects
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser


class ProjectsController:
    """
    This is the controller class which is used to handle all the logical and CURD operations.
    """

    @classmethod
    def add_project(cls, project_data: dict):
        """
        This function is used to add new project.
        :param project_data:
        :return int:
        """
        project = Projects.create(project_data)
        return project.id

    @classmethod
    def get_projects(cls, auth_user: AuthUser) -> list[dict]:
        """
        This function is used to get the list of projects of logged-in auth_user. If auth_user is Admin
        then this function will return all projects.
        :param auth_user:
        :return list[Projects]:
        """
        if auth_user.role == AuthUserController.ROLES.ADMIN.value:
            projects = Projects.query.all()
        else:
            projects = Projects.query.filter_by(user_id=auth_user.id)
        return [project.serialize() for project in projects]

    @classmethod
    def get_project_by_project_id(cls, project_id: int, auth_user: AuthUser) -> dict:
        """
        This function is used to get an project by project_id.
        :param project_id:
        :param auth_user:
        :return dict:
        """
        project = Projects.query.filter_by(id=project_id).first()
        cls.required_checks(auth_user, project)
        return project.serialize()

    @classmethod
    def update_project(cls, project_id: int, updated_project: dict, auth_user: AuthUser) -> dict:
        """
        This function is used to update the project. It required a valid project_id.
        :param project_id:
        :param updated_project:
        :param auth_user:
        :return dict:
        """
        project = Projects.query.filter_by(id=project_id).first()
        cls.required_checks(auth_user, project)
        project.update(updated_project)
        return {"msg": "success"}

    @classmethod
    def delete_project(cls, project_id, auth_user):
        """
        This function is used to delete a project by project_id.
        :param project_id:
        :param auth_user:
        :return dict:
        """
        project = Projects.query.filter_by(id=project_id).first()
        cls.required_checks(auth_user, project)
        Projects.delete(id=project_id)
        return {"msg": "success"}

    @classmethod
    def required_checks(cls, auth_user: AuthUser, project: Projects):
        """
        This function is used to check the required checks and raise a custom exception if any
        check failed. On custom exception server will return a response with defined error msg
        and status code.
        :param auth_user:
        :param project:
        :return:
        """
        if not project:
            raise EntityNotFoundError("Project Not Found!!!")
        if auth_user.role != AuthUserController.ROLES.ADMIN.value and project.user_id != auth_user.id:
            raise UnauthorizedUserError
