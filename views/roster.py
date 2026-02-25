import streamlit as st
from datetime import date


def render():
    from services.staff_service import get_all_staff
    from services.shift_service import get_shifts
    from services.roster_service import save_roster_entry

    st.header("Roster Management")

    staff_list = get_all_staff()
    shifts = get_shifts()

    if not staff_list:
        st.warning("No staff available.")
        return

    selected_staff = st.selectbox(
        "Select Staff",
        staff_list,
        format_func=lambda x: x.full_name
    )

    selected_date = st.date_input("Work Date", date.today())

    shift_options = [""] + [s.name for s in shifts]

    col1, col2 = st.columns(2)

    with col1:
        morning = st.selectbox("Morning Shift", shift_options)

    with col2:
        afternoon = st.selectbox("Afternoon Shift", shift_options)

    if st.button("Save Roster"):
        save_roster_entry(
            staff_id=selected_staff.id,
            work_date=selected_date,
            morning_shift=morning,
            afternoon_shift=afternoon
        )
        st.success("Roster saved.")