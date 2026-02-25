import streamlit as st

def render():
    from services.shift_service import get_shifts, update_shift_duration

    st.header("Shift Management")

    shifts = get_shifts()

    if not shifts:
        st.info("No shifts found.")
        return

    for shift in shifts:
        col1, col2 = st.columns([4, 2])

        with col1:
            st.write(f"**{shift.name}**")

        with col2:
            new_duration = st.number_input(
                f"Duration (hours)",
                min_value=0.0,
                value=float(shift.duration_hours),
                key=f"duration_{shift.id}"
            )

            if st.button("Update", key=f"update_{shift.id}"):
                update_shift_duration(shift.id, new_duration)
                st.success(f"{shift.name} updated.")