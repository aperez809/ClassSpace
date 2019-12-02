from ... import db
from .school import School
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.String(50),
                           index=False,
                           unique=False)
    last_name = db.Column(db.String(50),
                          index=False,
                          unique=False)
    email = db.Column(db.String(50),
                      index=False,
                      unique=False)
    password = db.Column(db.String(256),
                         index=False,
                         unique=False)
    school_name = db.Column(db.String(50),
                            index=False,
                            unique=False)
    school_id = db.Column(db.Integer,
                          db.ForeignKey(School.id),
                          index=False,
                          unique=False,
                          nullable=True)



    # def __init__(self, name: str, slug: str, school_name: str, school_id: int = None):
    #     self.id = None
    #     self.name = name
    #     self.slug = slug
    #     self.school_id = school_id
    #     self.school_name = school_name

    def __repr__(self):
        return f"User({self.id}, {self.first_name}, {self.last_name}, {self.email}, {self.password}, {self.school_name}, {self.school_id})"