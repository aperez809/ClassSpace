from ... import db

class Classroom(db.Model):

    __tablename__ = 'classrooms'

    id = db.Column(db.Integer,
                   primary_key=True)
    room_number = db.Column(db.String(10),
                            index=False,
                            unique=False)
    building_name = db.Column(db.String(50),
                              index=False,
                              unique=False)
    school_name = db.Column(db.String(100),
                            index=False,
                            unique=False)
    capacity = db.Column(db.Integer,
                         index=False,
                         unique=False)
    building_id = db.Column(db.Integer,
                            db.ForeignKey('buildings.id'),
                            index=False,
                            unique=False)
    school_id = db.Column(db.Integer,
                          db.ForeignKey('schools.id'),
                          index=False,
                          unique=False)

    # def __init__(self,
    #              room_number: str,
    #              building_name: str,
    #              school_name: str,
    #              capacity: int = None,
    #              building_id: int = None,
    #              school_id: int = None,
    #              ):
    #     self.id = None
    #     self.room_number = room_number  # Ex: "304", string type to handle cases like "032"
    #     self.capacity = capacity  # Number of people who can fit in classroom
    #     self.building_id = building_id  # Foreign key to the `buildings` table
    #     self.school_id = school_id  # Foreign key to the `schools` table
    #     self.building_name = building_name
    #     self.school_name = school_name

    def __str__(self):
        return f"{self.building_name} {self.room_number}"

    def __eq__(self, other):
        if isinstance(other, Classroom):
            return self.room_number == other.room_number and \
                   self.building_name == other.building_name and \
                   self.school_name == other.school_name
        return False

    def __hash__(self):
        return hash((self.room_number, self.building_name, self.school_name))
