from marshmallow import Schema, fields


class AddProjectSchema(Schema):
    """
    Schema to add project to the database.
    """

    project_name = fields.String(required=True)


class UpdateProjectSchema(Schema):
    """
    Schema to update the project.
    """

    project_name = fields.String(required=True)
