from ... import db
from .school import School


class Building(db.Model):

    __tablename__ = 'buildings'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     index=False,
                     unique=False)
    slug = db.Column(db.String(10),
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Building({self.name}, {self.slug}, {self.school_name})"

    def __eq__(self, other):
        if isinstance(other, Building):
            return self.name == other.name and self.slug == other.slug and self.school_name == other.school_name
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())
