from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class AddFileSchema(Schema):
    """
    Schema to add file to the database.
    """
    file_name = fields.String(required=True)
    project_id = fields.Integer(required=True)


class UpdateFileSchema(Schema):
    """
    Schema to update the file.
    """
    file_name = fields.String(required=False)
    project_id = fields.Integer(required=False)


class FileConversionSchema(Schema):
    """
    Schema to perform Conversion Operations
    """
    id = fields.Integer(required=True)
    output_file_name = fields.String(required=True)
    from_ext = fields.String(required=True)
    to_ext = fields.String(required=True)