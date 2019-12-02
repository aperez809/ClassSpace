from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, request, url_for, session
)
from flask.json import jsonify

from werkzeug.exceptions import abort

from flask_login import login_required, current_user
from .data.models.user import db, User
from .data.models.building import Building
from .data.models.classroom import Classroom


bp = Blueprint('dashboard', __name__)


@bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    """
    The dashboard page consists of 2 main pieces:
        1) Graph of hourly room availability for the current day
        2) Availability of rooms by building
    """

    today = datetime.today()
    # Get user's school so that we only query for buildings at that school
    user_school = User.query.filter(
        User.id == current_user.id
    ).first()

    # Get all buildings on campus so that we can display them each on the dashboard
    buildings = Building.query.filter(
        Building.school_id == user_school.school_id
    ).all()

    # Get count of available rooms by building, using the current time (+/- timezone offset)
    avail_rooms_by_building = db.execute(
        """SELECT count(*) FROM classroom_availability
            JOIN buildings on (classroom_availability.building_id = buildings.building_id) 
            WHERE weekday = ? start_time <= strftime(?) and end_time > strftime(?) and buildings.school_id = ?
            GROUP BY building_id 
        """, (
            today.weekday(),
            f"%H%M{user_school['tz_offset']}",
            f"%H%M{user_school['tz_offset']}",
            user_school['school_id']
        )
    ).fetchall()

    total_rooms = Classroom.query.filter()
    #     db.execute(
    #     'SELECT count(*) FROM classrooms GROUP BY building_id'
    # ).fetchall()

    return jsonify(
        buildings=buildings,
        avail_rooms_by_building=avail_rooms_by_building,
        total_rooms=total_rooms
    )


