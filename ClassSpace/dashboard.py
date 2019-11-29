from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, request, url_for, session
)
from flask.json import jsonify

from werkzeug.exceptions import abort

from ClassSpace.auth import login_required
from ClassSpace.db import get_db


bp = Blueprint('dashboard', __name__)


@bp.route('/', methods=['GET'])
@login_required
def get_dashboard():
    """
    The dashboard page consists of 2 main pieces:
        1) Graph of hourly room availability for the current day
        2) Availability of rooms by building
    """
    db = get_db()

    today = datetime.today()
    # Get user's school so that we only query for buildings at that school
    user_school = db.execute(
        'SELECT * FROM users WHERE id = ?', (session.get('user_id')),
    ).fetchone()

    # Get all buildings on campus so that we can display them each on the dashboard
    buildings = db.execute(
        'SELECT * FROM buildings WHERE school_id = ?', (user_school['school_id'])
    ).fetchall()

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

    total_rooms = db.execute(
        'SELECT count(*) FROM classrooms GROUP BY building_id'
    ).fetchall()

    return jsonify(
        buildings=buildings,
        avail_rooms_by_building=avail_rooms_by_building,
        total_rooms=total_rooms
    )


