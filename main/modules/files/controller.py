from main.custom_exceptions import EntityNotFoundError, UnauthorizedUserError
from main.modules.files.model import Files
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from flask import current_app
import os

class FilesController:
    """
    This is the controller class which is used to handle all the logical and CURD operations.
    """
    @classmethod
    def save_file(cls, request):
        f = request.files["file"]
        server_path = current_app.config.get('SERVER_PATH')
        file_path = os.path.join(server_path, f.filename)
        f.save(file_path)
        return file_path

    @classmethod
    def add_file(cls, file_data: dict):
        """
        This function is used to add new file.
        :param file_data:
        :return int:
        """
        file = Files.create(file_data)
        return file.id

    @classmethod
    def get_files(cls, auth_user: AuthUser) -> list[dict]:
        """
        This function is used to get the list of files of logged-in auth_user. If auth_user is Admin
        then this function will return all files.
        :param auth_user:
        :return list[Files]:
        """
        if auth_user.role == AuthUserController.ROLES.ADMIN.value:
            files = Files.query.all()
        else:
            files = Files.query.filter_by(user_id=auth_user.id)
        return [file.serialize() for file in files]

    @classmethod
    def get_file_by_file_id(cls, file_id: int, auth_user: AuthUser) -> dict:
        """
        This function is used to get an file by file_id.
        :param file_id:
        :param auth_user:
        :return dict:
        """
        file = Files.query.filter_by(id=file_id).first()
        cls.required_checks(auth_user, file)
        return file.serialize()

    @classmethod
    def update_file(cls, file_id: int, updated_file: dict, auth_user: AuthUser) -> dict:
        """
        This function is used to update the file. It required a valid file_id.
        :param file_id:
        :param updated_file:
        :param auth_user:
        :return dict:
        """
        file = Files.query.filter_by(id=file_id).first()
        cls.required_checks(auth_user, file)
        file.update(updated_file)
        return {"msg": "success"}

    @classmethod
    def delete_file(cls, file_id, auth_user):
        """
        This function is used to delete a file by file_id.
        :param file_id:
        :param auth_user:
        :return dict:
        """
        file = Files.query.filter_by(id=file_id).first()
        cls.required_checks(auth_user, file)
        Files.delete(id=file_id)
        return {"msg": "success"}

    @classmethod
    def required_checks(cls, auth_user: AuthUser, file: Files):
        """
        This function is used to check the required checks and raise a custom exception if any
        check failed. On custom exception server will return a response with defined error msg
        and status code.
        :param auth_user:
        :param file:
        :return:
        """
        if not file:
            raise EntityNotFoundError("File not found!!!")
        if auth_user.role != AuthUserController.ROLES.ADMIN.value and file.user_id != auth_user.id:
            raise UnauthorizedUserError
