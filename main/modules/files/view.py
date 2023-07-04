import os
from flask import jsonify, make_response, request, send_from_directory, send_file
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from main.modules.files.controller import FilesController
from main.modules.projects.controller import ProjectsController
from main.modules.files.converter import FileConversion
from main.modules.files.schema_validator import AddFileSchema, UpdateFileSchema, FileConversionSchema
from main.modules.auth.controller import AuthUserController
from main.utils import get_data_from_request_or_raise_validation_error, generate_uuid
from main.custom_exceptions import EntityAlreadyExistsError

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


class FilesUploadAPI(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        """
        This function is used to add new file to the database.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        file = request.files['file']
        project_id = request.form["project_id"]
        data = {"file_name": file.filename, "project_id": project_id}

        # Add validation for file or project not found

        data = get_data_from_request_or_raise_validation_error(AddFileSchema, data)
        if FilesController.get_file_by_file_name(data["file_name"], data["project_id"], auth_user):
            raise EntityAlreadyExistsError("A file with similar name already exists.")
        ProjectsController.get_project_by_project_id(data["project_id"], auth_user)
        data.update({"extension": os.path.splitext(file.filename)[-1]})
        data.update({"uid": generate_uuid()})
        data.update({"user_id": auth_user.id})
        file_location = FilesController.save_file(file, auth_user.id)
        data.update({"size": os.stat(file_location).st_size})
        data.update({"file_location": file_location})
        file_id = FilesController.add_file(data)
        response = make_response(jsonify({"message": "File added", "location": file_location, "id": file_id}), 201)
        return response


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
        # return send_from_directory(directory=os.path.dirname(file["file_location"]), path=file["file_name"], as_attachment=True)


class FilesConversionAPI(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        """
        This function is used to perform file conversion operations.
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(FileConversionSchema, request.json)
        output_file = data["output_file_name"] + "." + data["to_ext"]
        file_data = FilesController.get_file_by_file_id(data["id"], auth_user)

        if FilesController.get_file_by_file_name(output_file, file_data["project_id"], auth_user):
            raise EntityAlreadyExistsError(f"A file with name {output_file} already exists.")

        dest_file_location = FileConversion(file_data["file_location"], data["from_ext"], data["to_ext"], data["output_file_name"]).destination_file_path
        file_data.update({"file_name": os.path.basename(dest_file_location)})
        # Merge Updates in controller
        file_data.update({"extension": "."+data["to_ext"]})
        file_data.update({"file_location": dest_file_location})
        file_data.update({"uid": generate_uuid()})
        del file_data["created_at"]
        del file_data["updated_at"]
        del file_data["id"]
        del file_data["username"]
        file_data.update({"user_id": auth_user.id})

        file_id = FilesController.add_file(file_data)
        response = make_response(
            jsonify({"message": "File Converted Successfully.", "location": dest_file_location, "id": file_id}), 201
        )
        return response


file_namespace = Namespace("files", description="File Operations")
file_namespace.add_resource(GetProjectFilesApi, "/<int:project_id>")
file_namespace.add_resource(FilesUploadAPI, "")
file_namespace.add_resource(FileOperationAPI, "/<int:file_id>")
file_namespace.add_resource(FilesDownloadAPI, "/<string:uuid>/<string:file_name>")
file_namespace.add_resource(FilesConversionAPI, "/convert")