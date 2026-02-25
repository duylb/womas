from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from database.db import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    position = Column(String)

    salary_type = Column(String)  # hourly | package
    hourly_rate = Column(Float, nullable=True)
    package_salary = Column(Float, nullable=True)

    phone = Column(String)
    email = Column(String)
    address = Column(String)  # ✅ ADD THIS

    is_active = Column(Boolean, default=True)


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    duration_hours = Column(Float)


class Roster(Base):
    __tablename__ = "roster"

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    date = Column(Date)

    morning_shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=True)
    afternoon_shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=True)