import streamlit as st
import pandas as pd
from datetime import timedelta
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import ColumnsAutoSizeMode


# -------------------------------------------------
# STYLE
# -------------------------------------------------
st.markdown("""
<style>
.start-btn button {
    background-color: #2563eb;
    color: white;
    font-weight: 600;
}
.start-btn button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# DATE RANGE GENERATOR
# -------------------------------------------------
def generate_date_range(start_date, end_date):
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates


# -------------------------------------------------
# MAIN PAGE
# -------------------------------------------------
def render():
    from services.staff_service import get_all_staff

    st.header("Roster Management")

    # -------------------------------------------------
    # DATE CONTROLS
    # -------------------------------------------------
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    with col3:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        start_clicked = st.button("Start", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    if start_clicked:
        if start_date and end_date and start_date <= end_date:
            st.session_state["roster_start"] = start_date
            st.session_state["roster_end"] = end_date
        else:
            st.warning("Please select a valid date range.")
            return

    staff_list = get_all_staff()

    if not staff_list:
        st.info("No active staff available.")
        return

    if "roster_start" not in st.session_state:
        st.info("Select start and end dates, then press Start.")
        return

    start = st.session_state["roster_start"]
    end = st.session_state["roster_end"]
    date_range = generate_date_range(start, end)

    # -------------------------------------------------
    # BUILD TABLE DATA
    # -------------------------------------------------
    table_data = []

    for staff in staff_list:
        row = {
            "Full Name": staff.full_name,
            "Position": staff.position
        }

        for d in date_range:
            column_name = f"{d.strftime('%a')} {d.strftime('%d-%m')}"
            row[column_name] = ""

        table_data.append(row)

    df = pd.DataFrame(table_data)

    # -------------------------------------------------
    # AGGRID CONFIGURATION
    # -------------------------------------------------
    gb = GridOptionsBuilder.from_dataframe(df)

    # Freeze first 2 columns
    gb.configure_column("Full Name", pinned="left")
    gb.configure_column("Position", pinned="left")

    # Center align header and cell text
    gb.configure_default_column(
        cellStyle={"textAlign": "center"},
        headerClass="center-header"
    )

    gb.configure_grid_options(
        suppressColumnVirtualisation=False,
        domLayout="normal"
    )

    grid_options = gb.build()

    st.divider()
    st.subheader("Roster Schedule")

    AgGrid(
        df,
        gridOptions=grid_options,
        height=600,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.NO_AUTOSIZE,
        fit_columns_on_grid_load=False,
    )