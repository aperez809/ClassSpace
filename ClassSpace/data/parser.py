from models.building import Building
from models.classroom import Classroom
from models.course_slot import CourseSlot
from models.school import School
from models.weekday import DayOfWeekEnum
import json
from datetime import datetime
import csv
import os


class MasterParser:
    def __init__(self):
        self.schools = {School('Northeastern University', "-4")}  # For now, default to only include NEU
        self.buildings = set()
        self.classrooms = set()
        self.course_slots = set()

    def parse_raw_schedule(self):

        curr_dir = os.path.dirname(__file__)
        with open(os.path.join(curr_dir, 'data_files/raw_schedule.json'), 'r') as f:
            course_list = json.loads(f.read())

        for course in course_list:
            self.__build_model_objs(course)

    def __build_model_objs(self, course) -> set():
        """Use building-related fields to construct a Building Object"""

        room_capacity = course['maximumEnrollment']
        school_name = 'Northeastern University'
        for elem in course['meetingsFaculty']:
            meeting_time = elem['meetingTime']

            # Skip any course slots that are for Final Exams
            if meeting_time['meetingTypeDescription'] == 'Final Exam' or not meeting_time['beginTime']:
                continue

            # Buildings can just be created and added to the set
            building = Building(
                name=meeting_time['buildingDescription'],
                slug=meeting_time['building'],
                school_name=school_name,
                school_id=1
            )
            self.buildings.add(building)

            # same for Classrooms
            classroom = Classroom(
                room_number=meeting_time['room'],
                building_name=meeting_time['building'],
                school_name=school_name,
                school_id=1,
                capacity=room_capacity
            )
            self.classrooms.add(classroom)

            # CourseSlots are based on both time of day and day of week
            # i.e. a `meeting_time` object can have multiple CourseSlots in it
            # Helper method to create the individual slots
            self.__create_course_slots(meeting_time)

        return self.__convert_to_csvs()

    def __convert_to_csvs(self):
        field_names = ['buildings', 'classrooms', 'course_slots']
        vals = [self.buildings, self.classrooms, self.course_slots]

        for idx in range(len(field_names)):
            set_to_list = list(vals[idx])
            keys = set_to_list[0].__dict__.keys()
            with open(f'{field_names[idx]}.csv', 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows([x.__dict__ for x in set_to_list])

    def __create_course_slots(self, meeting_time):

        # Map of days (as described in JSON) to DayOfWeekEnum val
        days = {
            'monday': DayOfWeekEnum.MONDAY,
            'tuesday': DayOfWeekEnum.TUESDAY,
            'wednesday': DayOfWeekEnum.WEDNESDAY,
            'thursday': DayOfWeekEnum.THURSDAY,
            'friday': DayOfWeekEnum.FRIDAY,
            'saturday': DayOfWeekEnum.SATURDAY,
            'sunday': DayOfWeekEnum.SUNDAY
        }

        school_name = 'Northeastern University'

        # Converting string values in JSON to datetime objects
        try:
            start_time = datetime.strptime(meeting_time['beginTime'], '%H%M').time()
            end_time = datetime.strptime(meeting_time['endTime'], '%H%M').time()
            start_date = datetime.strptime(meeting_time['startDate'], '%m/%d/%Y').date()
            end_date = datetime.strptime(meeting_time['endDate'], '%m/%d/%Y').date()
        except:
            print(meeting_time)
            raise TypeError

        for day, enum_val in days.items():
            if meeting_time[day]:
                self.course_slots.add(
                    CourseSlot(
                        start_time=start_time,
                        end_time=end_time,
                        start_date=start_date,
                        end_date=end_date,
                        weekday=enum_val,
                        school_name=school_name,
                        building_name=meeting_time['buildingDescription'],
                        classroom_number=meeting_time['room']
                    )
                )


p = MasterParser()
p.parse_raw_schedule()




