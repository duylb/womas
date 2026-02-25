import streamlit as st
from datetime import date
from services.staff_service import get_all_staff
from services.shift_service import get_shifts
from services.roster_service import save_roster_entry

def render():
    st.title("Roster Management")

    staff_list = get_all_staff()
    shifts = get_shifts()

    shift_dict = {s.name: s.id for s in shifts}

    selected_date = st.date_input("Select Date", date.today())

    for staff in staff_list:
        st.subheader(staff.full_name)

        col1, col2 = st.columns(2)

        morning = col1.selectbox(
            "Morning",
            [""] + list(shift_dict.keys()),
            key=f"m{staff.id}"
        )

        afternoon = col2.selectbox(
            "Afternoon",
            [""] + list(shift_dict.keys()),
            key=f"a{staff.id}"
        )

        if st.button("Save", key=f"s{staff.id}"):
            save_roster_entry(
                staff.id,
                selected_date,
                shift_dict.get(morning),
                shift_dict.get(afternoon)
            )
            st.success("Saved")