import streamlit as st
import pandas as pd
from datetime import timedelta
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import ColumnsAutoSizeMode


# =====================================================
# GLOBAL STYLES
# =====================================================

st.markdown("""
<style>

/* --- Start Button Style --- */
div.stButton > button {
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    height: 42px;
}
div.stButton > button:hover {
    background-color: #1e40af;
}

/* --- AGGrid Header Alignment --- */
.ag-header-cell {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.ag-header-cell-label {
    justify-content: center !important;
    align-items: center !important;
}

/* --- Optional: Slightly darker pinned columns --- */
.ag-pinned-left-cols-container {
    background-color: #0f172a !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER
# =====================================================

def generate_date_range(start_date, end_date):
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates


# =====================================================
# MAIN RENDER FUNCTION
# =====================================================

def render():
    from services.staff_service import get_all_staff

    st.header("Roster Management")

    # -------------------------------------------------
    # DATE CONTROLS (PERFECT ALIGNMENT)
    # -------------------------------------------------
    col1, col2, col3 = st.columns([3, 3, 1.2])

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    with col3:
        st.markdown(
            '<div style="display:flex; align-items:flex-end; height:100%;">',
            unsafe_allow_html=True
        )
        start_clicked = st.button("Start", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------
    # HANDLE START CLICK
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

    if "roster_start" not in st.session_state:
        st.info("Select start and end dates, then press Start.")
        return

    # -------------------------------------------------
    # BUILD DATE RANGE
    # -------------------------------------------------
    start = st.session_state["roster_start"]
    end = st.session_state["roster_end"]
    date_range = generate_date_range(start, end)

    # -------------------------------------------------
    # BUILD DATAFRAME
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
    gb.configure_column("Full Name", pinned="left", width=180)
    gb.configure_column("Position", pinned="left", width=140)

    # Center align everything
    gb.configure_default_column(
        cellStyle={"textAlign": "center"},
        headerClass="center-header",
        resizable=True
    )

    gb.configure_grid_options(
        domLayout="normal",
        suppressColumnVirtualisation=False
    )

    grid_options = gb.build()

    # -------------------------------------------------
    # RENDER GRID
    # -------------------------------------------------
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