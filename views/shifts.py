import streamlit as st
from services.shift_service import get_all_shifts, update_shift_duration


def render():
    st.header("Shift Management")

    shifts = get_all_shifts()

    if not shifts:
        st.info("No shifts found.")
        return

    for shift in shifts:
        col1, col2 = st.columns([4, 2])

        with col1:
            st.write(f"**{shift.name}**")

        with col2:
            new_duration = st.number_input(
                f"Duration (hours) - {shift.name}",
                min_value=0.0,
                value=float(shift.duration),
                key=f"duration_{shift.id}"
            )

            if st.button("Update", key=f"update_{shift.id}"):
                update_shift_duration(shift.id, new_duration)
                st.success(f"{shift.name} updated.")