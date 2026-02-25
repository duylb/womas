import streamlit as st
import pandas as pd
from datetime import timedelta


def generate_date_range(start_date, end_date):
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def render():
    from services.staff_service import get_all_staff

    st.header("Roster Management")

    # -------------------------------------------------
    # DATE SELECTION
    # -------------------------------------------------
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    with col3:
        start_clicked = st.button("Start", width="stretch")

    # -------------------------------------------------
    # STORE DATE RANGE IN SESSION
    # -------------------------------------------------
    if start_clicked:
        if start_date and end_date and start_date <= end_date:
            st.session_state["roster_start"] = start_date
            st.session_state["roster_end"] = end_date
        else:
            st.warning("Please select a valid date range.")
            return

    # -------------------------------------------------
    # LOAD STAFF
    # -------------------------------------------------
    staff_list = get_all_staff()

    if not staff_list:
        st.info("No active staff available.")
        return

    # -------------------------------------------------
    # IF DATE RANGE SELECTED → BUILD TABLE
    # -------------------------------------------------
    if "roster_start" in st.session_state and "roster_end" in st.session_state:

        start = st.session_state["roster_start"]
        end = st.session_state["roster_end"]

        date_range = generate_date_range(start, end)

        # Build table data
        table_data = []

        for staff in staff_list:
            row = {
                "Full Name": staff.full_name,
                "Position": staff.position
            }

            for d in date_range:
                column_name = f"{d.strftime('%a')} {d.strftime('%d-%m')}"
                row[column_name] = ""  # placeholder for shift

            table_data.append(row)

        df = pd.DataFrame(table_data)

        st.divider()
        st.subheader("Roster Schedule")

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    else:
        st.info("Select start and end dates, then press Start.")