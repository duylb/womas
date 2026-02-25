import streamlit as st
import pandas as pd
from datetime import timedelta
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import ColumnsAutoSizeMode


# =====================================================
# SHIFT DROPDOWN RENDERER (COMPATIBLE WITH 1.2.1)
# =====================================================

shift_renderer = JsCode("""
function(params) {
    const position = (params.data.Position || "").toLowerCase();
    const isMorning = params.colDef.field.endsWith("_M");

    let options = [""];

    if (position.includes("service")) {
        options = isMorning
            ? ["", "S1", "S2", "S3"]
            : ["", "S4", "S5", "S6"];
    }
    else if (position.includes("kitchen")) {
        options = isMorning
            ? ["", "B1", "B2", "B3"]
            : ["", "B4", "B5", "B6"];
    }
    else {
        return "";
    }

    const select = document.createElement("select");
    select.style.width = "100%";
    select.style.height = "100%";
    select.style.textAlign = "center";
    select.style.border = "none";
    select.style.background = "transparent";

    options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt;
        option.text = opt;
        if (params.value === opt) option.selected = true;
        select.appendChild(option);
    });

    select.addEventListener("change", function() {
        params.node.setDataValue(params.column.getId(), this.value);
    });

    return select;
}
""")


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
# MAIN
# =====================================================

def render():

    from services.staff_service import get_all_staff

    st.header("Roster Management")

    # DATE CONTROLS
    st.markdown("#### Select Date Range")

    col1, col2, col3 = st.columns([3, 3, 1.2])

    with col1:
        st.markdown("Start Date")
        start_date = st.date_input("start", label_visibility="collapsed")

    with col2:
        st.markdown("End Date")
        end_date = st.date_input("end", label_visibility="collapsed")

    with col3:
        st.markdown("&nbsp;")
        start_clicked = st.button("Start", width="stretch")

    if start_clicked:
        if start_date and end_date and start_date <= end_date:
            st.session_state["roster_start"] = start_date
            st.session_state["roster_end"] = end_date
        else:
            st.warning("Please select valid dates.")
            return

    staff_list = get_all_staff()

    if not staff_list:
        st.info("No active staff.")
        return

    if "roster_start" not in st.session_state:
        st.info("Select dates and press Start.")
        return

    start = st.session_state["roster_start"]
    end = st.session_state["roster_end"]

    date_range = generate_date_range(start, end)

    # BUILD DATAFRAME
    table_data = []

    for staff in staff_list:
        row = {
            "Full Name": staff.full_name,
            "Position": staff.position
        }

        for d in date_range:
            lbl = d.strftime("%d-%m")
            row[f"{lbl}_M"] = ""
            row[f"{lbl}_A"] = ""

        table_data.append(row)

    df = pd.DataFrame(table_data)

    # =====================================================
    # GRID BUILDER (WORKING VERSION FOR 1.2.1)
    # =====================================================

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_column("Full Name", pinned="left", width=180)
    gb.configure_column("Position", pinned="left", width=130)

    for d in date_range:
        lbl = d.strftime("%d-%m")

        gb.configure_column(
            f"{lbl}_M",
            header_name="M",
            width=90,
            editable=True,
            cellEditor="agSelectCellEditor",
            cellEditorParams={
                "values": ["", "S1", "S2", "S3", "B1", "B2", "B3"]
            }
        )

        gb.configure_column(
            f"{lbl}_A",
            header_name="A",
            width=90,
            editable=True,
            cellEditor="agSelectCellEditor",
            cellEditorParams={
                "values": ["", "S4", "S5", "S6", "B4", "B5", "B6"]
            }
        )

    gb.configure_default_column(
        cellStyle={"textAlign": "center"},
        resizable=False
    )

    grid_options = gb.build()