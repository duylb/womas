from database.db import SessionLocal
from database.models import Shift

DEFAULT_SHIFTS = [
    "Q1","Q2","Q3",
    "S1","S2","S3",
    "C1","C2","C3",
    "B1","B2","B3","B4","B5","B6"
]

def init_shifts():
    db = SessionLocal()
    existing = db.query(Shift).count()

    if existing == 0:
        for name in DEFAULT_SHIFTS:
            db.add(Shift(name=name, duration_hours=8))
        db.commit()
    db.close()

def get_shifts():
    db = SessionLocal()
    shifts = db.query(Shift).all()
    db.close()
    return shifts

def update_shift_duration(shift_id, duration):
    db = SessionLocal()
    shift = db.query(Shift).get(shift_id)
    shift.duration_hours = duration
    db.commit()
    db.close()