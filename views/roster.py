import streamlit as st
import pandas as pd
from datetime import timedelta
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import ColumnsAutoSizeMode


# =====================================================
# STYLES
# =====================================================

st.markdown("""
<style>
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

.ag-header-cell {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.ag-header-cell-label {
    justify-content: center !important;
    align-items: center !important;
}

.ag-pinned-left-cols-container {
    background-color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SHIFT DROPDOWN RENDERER
# =====================================================

sshift_renderer = JsCode("""
class ShiftSelector {
    init(params) {
        const position = (params.data.Position || "").toLowerCase();
        const isMorning = params.colDef.field.endsWith("_M");

        let options = [""];

        if (position === "service") {
            options = isMorning
                ? ["", "S1", "S2", "S3"]
                : ["", "S4", "S5", "S6"];
        }
        else if (position === "kitchen") {
            options = isMorning
                ? ["", "B1", "B2", "B3"]
                : ["", "B4", "B5", "B6"];
        }
        else {
            // Manager or Admin → no dropdown
            this.eGui = document.createElement("div");
            this.eGui.innerHTML = "";
            return;
        }

        this.eGui = document.createElement("select");
        this.eGui.style.width = "100%";
        this.eGui.style.height = "100%";
        this.eGui.style.textAlign = "center";
        this.eGui.style.background = "transparent";
        this.eGui.style.border = "none";

        options.forEach(opt => {
            const option = document.createElement("option");
            option.value = opt;
            option.text = opt;
            if (params.value === opt) option.selected = true;
            this.eGui.appendChild(option);
        });

        this.eGui.addEventListener("change", () => {
            params.node.setDataValue(
                params.column.getId(),
                this.eGui.value
            );
        });
    }

    getGui() {
        return this.eGui;
    }

    refresh(params) {
        return false;
    }
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

    # AGGRID CONFIG
    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_column("Full Name", pinned="left", width=180)
    gb.configure_column("Position", pinned="left", width=130)

    for d in date_range:
        lbl = d.strftime("%d-%m")
        gb.configure_column(
            f"{lbl}_M",
            header_name="M",
            width=70,
            cellRenderer=shift_renderer
        )
        gb.configure_column(
            f"{lbl}_A",
            header_name="A",
            width=70,
            cellRenderer=shift_renderer
        )

    gb.configure_default_column(
        cellStyle={"textAlign": "center"},
        resizable=False
    )

    gb.configure_grid_options(domLayout="normal")

    grid_options = gb.build()

    # GROUP HEADERS
    built_defs = grid_options["columnDefs"]

    pinned_defs = [c for c in built_defs if c.get("pinned") == "left"]
    date_map = {c["field"]: c for c in built_defs if "_" in c.get("field", "")}

    date_groups = []

    for d in date_range:
        lbl = d.strftime("%d-%m")
        header = f"{d.strftime('%a')} {lbl}"

        date_groups.append({
            "headerName": header,
            "children": [
                date_map[f"{lbl}_M"],
                date_map[f"{lbl}_A"]
            ]
        })

    grid_options["columnDefs"] = [
        {"headerName": "", "children": pinned_defs}
    ] + date_groups

    st.divider()
    st.subheader("Roster Schedule")

    AgGrid(
        df,
        gridOptions=grid_options,
        height=650,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.NO_AUTOSIZE,
        fit_columns_on_grid_load=False,
    )