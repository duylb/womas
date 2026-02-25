import streamlit as st
from services.shift_service import get_shifts, update_shift_duration, init_shifts

def render():
    st.title("Shift Management")

    init_shifts()

    shifts = get_shifts()

    for shift in shifts:
        col1, col2 = st.columns([2,2])
        col1.write(shift.name)
        duration = col2.number_input(
            f"Duration for {shift.name}",
            value=float(shift.duration_hours),
            key=shift.id
        )

        if st.button("Update", key=f"u{shift.id}"):
            update_shift_duration(shift.id, duration)
            st.success("Updated")
            st.rerun()