from main.db import BaseModel, db
from datetime import datetime

class Files(BaseModel):
    """
    Model for files.
    """

    __tablename__ = "files"

    file_name = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(5), nullable=False)
    # date_saved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    file_location = db.Column(db.Text, nullable=False)
    uid = db.Column(db.String(32), nullable = False)
    size = db.Column(db.Float, nullable = False)
    project_id = db.Column(db.ForeignKey('projects.id'))
    user_id = db.Column(db.ForeignKey("auth_user.id"))

    user = db.relationship("AuthUser", backref=db.backref("files", lazy=True))
    project = db.relationship("Projects", backref=db.backref("files", lazy=True))


    def serialize(self) -> dict:
        """
        Override serialize function to add extra functionality
        :return:
        """
        dict_data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "user_id"}
        dict_data["username"] = self.user.username if self.user else None
        return dict_data
    

    # def serialize_projects(self):
    #     if self.user_id:
    #         dict_user = self.project_owner.serialize_user_bis()

    #     return {
    #             "id": self.id,
    #             "project_name": self.project_name,
    #             "user_id": dict_user
    #     }
