from sqlalchemy.exc import IntegrityError
from database.db import SessionLocal
from database.models import Staff

def get_all_staff():
    db = SessionLocal()
    staff = db.query(Staff).filter(Staff.is_active == True).all()
    db.close()
    return staff

def add_staff(data):
    db = SessionLocal()
    try:
        staff = Staff(**data)
        db.add(staff)
        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close()

def deactivate_staff(staff_id):
    db = SessionLocal()
    staff = db.query(Staff).get(staff_id)
    staff.is_active = False
    db.commit()
    db.close()