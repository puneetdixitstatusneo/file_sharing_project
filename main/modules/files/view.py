import os
from flask import jsonify, make_response, request, send_from_directory, send_file
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from main.modules.files.controller import FilesController
from main.modules.projects.controller import ProjectsController

from main.modules.files.schema_validator import AddFileSchema, AddFileNameSchema, UpdateFileSchema, FileConversionSchema
from main.modules.auth.controller import AuthUserController
from main.utils import get_data_from_request_or_raise_validation_error, generate_uuid
from main.custom_exceptions import EntityAlreadyExistsError, CustomValidationError

class GetProjectFilesApi(Resource):
    method_decorators = [jwt_required()]

    def get(self, project_id: int):
        """
        This function is used to get the list of fies.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = FilesController.get_file_by_project_id(project_id, auth_user)
        return jsonify(response)
    

class GetConvertedFiles(Resource):
    method_decorators = [jwt_required()]

    def get(self, converted_uuid: str):
        """
        This function is used to get the list of converted.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = FilesController.get_file_by_converted_uuid(converted_uuid, auth_user)
        return jsonify(response)


class FilesUploadAPI(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        """
        This function is used to add new file to the database.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()

        

        file = request.files.get('file')
        project_id = request.form.get('project_id')
        if file and project_id:
            data = {"file_name": file.filename if file is not None else file, "project_id": project_id}
            # data = get_data_from_request_or_raise_validation_error(AddFileNameSchema, data)

            if FilesController.get_file_by_file_name(data["file_name"], data["project_id"], auth_user):
                raise EntityAlreadyExistsError("A file with similar name already exists.")
            ProjectsController.get_project_by_project_id(data["project_id"], auth_user)
            data.update({"extension": os.path.splitext(file.filename)[-1]})
            data.update({"uid": generate_uuid()})
            data.update({"conversion_uuid": generate_uuid()})

            data.update({"user_id": auth_user.id})
            file_location = FilesController.save_file(file, auth_user.id)
            data.update({"size": os.stat(file_location).st_size})
            data.update({"file_location": file_location})
            file_id = FilesController.add_file(data)
            response = make_response(jsonify({"message": "File added", "id": file_id}), 201)
            return response
        raise  CustomValidationError("File and project_id both are required parameters.")



class FileOperationAPI(Resource):
    method_decorators = [jwt_required()]

    def put(self, file_id: int):
        """
        This function is used to update the file by file_id
        :param file_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(UpdateFileSchema, request.json)
        ProjectsController.get_project_by_project_id(data["project_id"], auth_user)
        response = FilesController.update_file(file_id, data, auth_user)
        return jsonify(response)


    def delete(self, file_id: int):
        """
        This function is used to delete the file by file_id.
        :param file_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = FilesController.delete_file(file_id, auth_user)
        return jsonify(response)


class FilesDownloadAPI(Resource):
    # method_decorators = [jwt_required()]

    def get(self, uuid : str, file_name :str):
        """
        This function is used to download a file.
        :return:
        """
        file = FilesController.get_file_by_uuid(uuid)
        return send_file(file["file_location"], download_name=file["file_name"],mimetype='text/plain')



class FilesConversionAPI(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        """
        This function is used to perform file conversion operations.
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(FileConversionSchema, request.json)
        response = FilesController.add_converted_file(data, auth_user)
        return response



file_namespace = Namespace("files", description="File Operations")
file_namespace.add_resource(GetProjectFilesApi, "/<int:project_id>")
file_namespace.add_resource(GetConvertedFiles, "/<string:converted_uuid>")
file_namespace.add_resource(FilesUploadAPI, "")
file_namespace.add_resource(FileOperationAPI, "/<int:file_id>")
file_namespace.add_resource(FilesDownloadAPI, "/<string:uuid>/<string:file_name>")
file_namespace.add_resource(FilesConversionAPI, "/convert")





# Select Project if only one project is there
# Show all file Actions inside File Action
# Convert Dropdown for Convert To
# Show already Converted Files
# Add functionality to add people to projects
# Edit and Delete Project should be available to only project owner and Admin
# Implement multiple Delete files
