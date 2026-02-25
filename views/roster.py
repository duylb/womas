import streamlit as st
from datetime import date
from services.staff_service import get_all_staff
from services.shift_service import get_all_shifts
from services.roster_service import save_roster_entry


def render():
    st.header("Roster Management")

    staff_list = get_all_staff()
    shifts = get_all_shifts()

    if not staff_list:
        st.warning("No staff found. Please add staff first.")
        return

    selected_staff = st.selectbox(
        "Select Staff",
        staff_list,
        format_func=lambda x: x.full_name
    )

    selected_date = st.date_input("Select Date", date.today())

    shift_options = [""] + [shift.name for shift in shifts]

    col1, col2 = st.columns(2)

    with col1:
        morning_shift = st.selectbox("Morning Shift", shift_options)

    with col2:
        afternoon_shift = st.selectbox("Afternoon Shift", shift_options)

    if st.button("Save Roster"):
        save_roster_entry(
            staff_id=selected_staff.id,
            work_date=selected_date,
            morning_shift=morning_shift,
            afternoon_shift=afternoon_shift
        )
        st.success("Roster saved successfully.")