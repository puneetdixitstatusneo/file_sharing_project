import os
from datetime import datetime
from main.custom_exceptions import EntityNotFoundError, UnauthorizedUserError, EntityAlreadyExistsError
from main.modules.files.model import Files
from main.modules.auth.controller import AuthUserController
from main.modules.auth.model import AuthUser
from flask import current_app, make_response, jsonify
from main.utils import generate_uuid
from main.modules.files.converter import FileConversion


class FilesController:
    """
    This is the controller class which is used to handle all the logical and CURD operations.
    """
    @classmethod
    def save_file(cls, file, user_id):
        server_path = current_app.config.get('SERVER_PATH')
        now = datetime.now().date().strftime("%Y-%m-%d")
        os.makedirs(os.path.join(server_path, str(user_id), now), exist_ok=True)
        file_path = os.path.join(server_path, str(user_id), now, file.filename)
        file.save(file_path)
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
    def get_file_by_file_name(cls, file_name: str, project_id: int, auth_user: AuthUser) -> dict:
        """
        This function is used to get an file by file_name.
        :param file_name:
        :param auth_user:
        :return dict:
        """
        files = Files.query.filter_by(file_name=file_name, project_id = project_id)
        return [file.serialize() for file in files]


    @classmethod
    def get_file_by_project_id(cls, project_id: int, auth_user: AuthUser) -> dict:
        """
        This function is used to get an file by project_id.
        :param project_id:
        :param auth_user:
        :return dict:
        """
        files = Files.query.filter_by(project_id=project_id)
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
    def get_file_by_uuid(cls, uuid: str) -> dict:
        """
        This function is used to get an file by UUID.
        :param uid:
        :param auth_user:
        :return dict:
        """
        file = Files.query.filter_by(uid=uuid).first()
        # cls.required_checks(auth_user, file)
        return file.serialize()
    
    @classmethod
    def get_file_by_converted_uuid(cls, converted_uuid:str, auth_user: AuthUser) -> dict:
        """
        This function is used to get an file by UUID.
        :param uid:
        :param auth_user:
        :return dict:
        """
        files = Files.query.filter_by(conversion_uuid=converted_uuid)
        # cls.required_checks(auth_user, file)
        return [file.serialize() for file in files]



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
        if os.path.exists(file.file_location):
            os.remove(file.file_location)
        Files.delete(id=file_id)
        return {"msg": "success"}
    
    @classmethod
    def add_converted_file(cls, data, auth_user):
        file_data = cls.get_file_by_file_id(data["id"], auth_user)

        if data["from_ext"].startswith("."):
            data["from_ext"] = data["from_ext"][1:]
        if data["to_ext"].startswith("."):
            data["to_ext"] = data["to_ext"][1:]

        output_file = data["output_file_name"] + "." + data["to_ext"]

        if FilesController.get_file_by_file_name(output_file, file_data["project_id"], auth_user):
            raise EntityAlreadyExistsError(f"A file with name {output_file} already exists.")

        fc = FileConversion(file_data["file_location"], data["from_ext"], data["to_ext"], data["output_file_name"])
        if not fc.status:
            raise EntityNotFoundError(f'File Conversion not possible for {data["from_ext"]} to {data["to_ext"]} yet')
            # response = make_response(jsonify({"message": f'File Conversion not possible for {data["from_ext"]} to {data["to_ext"]} yet',}), 201)
            # return response
        dest_file_location = fc.destination_file_path
        file_data.update({"file_name": os.path.basename(dest_file_location),
                          "extension": "."+data["to_ext"],
                          "file_location": dest_file_location,
                          "uid": generate_uuid(),
                          "user_id": auth_user.id, 
                          "conversion_uuid": file_data["conversion_uuid"]})

        del file_data["created_at"]
        del file_data["updated_at"]
        del file_data["id"]
        del file_data["username"]

        file_id = cls.add_file(file_data)
        response = make_response(jsonify({"message": "File Converted Successfully.", "id": file_id}), 201)
        return response


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
        

