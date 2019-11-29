from datetime import datetime
from .weekday import DayOfWeekEnum
import time

class CourseSlot:

    def __init__(
            self,
            start_time: time,
            end_time: time,
            start_date: datetime,
            end_date: datetime,
            weekday: DayOfWeekEnum,
            school_name: str,
            building_name: str,
            classroom_number: str,
            school_id: int = None,
            building_id: int = None,
            classroom_id: int = None,
    ):
        self.start_time = start_time  # Beginning of course slot in HH:MM AM/PM format
        self.end_time = end_time  # Ending of course slot in HH:MM AM/PM format
        self.start_date = start_date  # First day of course slot in some ISO datetime format
        self.end_date = end_date  # Last day of course slot in some ISO datetime format
        self.weekday = weekday  # Day of week for the course slot
        self.school_id = school_id  # Foreign key for `schools` table
        self.building_id = building_id  # Foreign key for the `buildings` table
        self.classroom_id = classroom_id  # Foreign key for the `classrooms` table
        self.school_name= school_name
        self.building_name = building_name
        self.classroom_number = classroom_number

    def __str__(self):
        return f"{self.classroom_number}: {self.weekday} {self.start_time}-{self.end_time}"
