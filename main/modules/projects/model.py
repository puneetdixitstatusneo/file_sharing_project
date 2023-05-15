from main.db import BaseModel, db


class Projects(BaseModel):
    """
    Model for projects.
    """

    __tablename__ = "projects"

    project_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.ForeignKey("auth_user.id"))

    user = db.relationship("AuthUser", backref=db.backref("projects", lazy=True))


    def serialize(self) -> dict:
        """
        Override serialize function to add extra functionality
        :return:
        """
        dict_data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "user_id"}
        dict_data["username"] = self.user.username if self.user else None
        return dict_data


