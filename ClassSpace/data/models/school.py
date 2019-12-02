from ... import db


class School(db.Model):

    __tablename__ = 'schools'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     index=False,
                     unique=False,
                     nullable=False)
    tz_offset = db.Column(db.String(5),
                          index=False,
                          unique=False,
                          nullable=False)

    # def __init__(self, name: str, tz_offset: str):
    #     self.id = None
    #     self.name = name
    #     self.tz_offset = tz_offset

    def __str__(self):
        return self.name
