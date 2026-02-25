from database.db import SessionLocal
from database.models import Staff, Shift, Roster
from sqlalchemy import extract

def calculate_monthly_payroll(month, year):
    db = SessionLocal()
    results = []

    staff_list = db.query(Staff).filter(Staff.is_active == True).all()

    for staff in staff_list:
        entries = db.query(Roster).filter(
            Roster.staff_id == staff.id,
            extract('month', Roster.date) == month,
            extract('year', Roster.date) == year
        ).all()

        total_hours = 0

        for e in entries:
            if e.morning_shift_id:
                shift = db.query(Shift).get(e.morning_shift_id)
                total_hours += shift.duration_hours
            if e.afternoon_shift_id:
                shift = db.query(Shift).get(e.afternoon_shift_id)
                total_hours += shift.duration_hours

        if staff.salary_type == "hourly":
            salary = total_hours * (staff.hourly_rate or 0)
        else:
            salary = staff.package_salary or 0

        results.append({
            "name": staff.full_name,
            "position": staff.position,
            "total_hours": total_hours,
            "salary": salary,
            "email": staff.email
        })

    db.close()
    return results

def calculate_payroll():
    from datetime import datetime
    today = datetime.today()
    return calculate_monthly_payroll(today.month, today.year)