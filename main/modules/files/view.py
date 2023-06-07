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

class FilesApi(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        """
        This function is used to get the list of fies.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = FilesController.get_files(auth_user)
        return jsonify(response)

    def post(self):
        """
        This function is used to add new file to the database.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        file = request.files['file']
        project_id = request.form["project_id"]
        data = {"file_name": file.filename, "project_id": project_id}
        data = get_data_from_request_or_raise_validation_error(AddFileSchema, data)
        ProjectsController.get_project_by_project_id(data["project_id"], auth_user)
        data.update({"extension": os.path.splitext(file.filename)[-1]})
        data.update({"uid": generate_uuid()})
        data.update({"user_id": auth_user.id})
        file_location = FilesController.save_file(request, auth_user.id)
        size = os.stat(file_location).st_size
        data.update({"size": size})
        data.update({"file_location": file_location})
        file_id = FilesController.add_file(data)
        response = make_response(
            jsonify({"message": "File added", "location": file_location, "id": file_id}), 201
        )
        response.headers["Location"] = f"file_location"
        return response


class FilesApi2(Resource):
    method_decorators = [jwt_required()]

    def get(self, file_id: int):
        """
        This function is used to get the particular file by file_id
        :param file_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = FilesController.get_file_by_file_id(file_id, auth_user)
        return jsonify(response)

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


class FilesApi3(Resource):
    method_decorators = [jwt_required()]

    def get(self, uuid : str, file_name :str):
        """
        This function is used to download a file.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        file = FilesController.get_file_by_uuid(uuid, auth_user)
        print(os.path.dirname(file["file_location"]))
        print(file["file_name"])
        # if file["extension"].lower() in [".json", ".xml"]:
        #     return send_from_directory(directory=file["file_location"], path=file["file_name"], as_attachment=False)
        # else:
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
        file_data = FilesController.get_file_by_file_link(data["file_link"], auth_user)
        dest_file_location = FileConversion(file_data["file_location"], data["from_ext"], data["to_ext"]).destination_file_path
        file_data.update({"file_name": os.path.basename(dest_file_location)})
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
            jsonify({"message": "File Conversion Successfull.", "location": dest_file_location, "id": file_id}), 201
        )
        response.headers["Location"] = f"file_location"
        return response



file_namespace = Namespace("files", description="File Operations")
file_namespace.add_resource(FilesApi, "")
file_namespace.add_resource(FilesApi2, "/<int:file_id>")
file_namespace.add_resource(FilesApi3, "/<string:uuid>/<string:file_name>")
file_namespace.add_resource(FilesConversionAPI, "/convert")