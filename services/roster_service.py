from database.db import SessionLocal
from database.models import Roster
from datetime import date

def save_roster_entry(staff_id, work_date, morning_id, afternoon_id):
    db = SessionLocal()

    existing = db.query(Roster).filter_by(
        staff_id=staff_id,
        date=work_date
    ).first()

    if existing:
        existing.morning_shift_id = morning_id
        existing.afternoon_shift_id = afternoon_id
    else:
        db.add(Roster(
            staff_id=staff_id,
            date=work_date,
            morning_shift_id=morning_id,
            afternoon_shift_id=afternoon_id
        ))

    db.commit()
    db.close()