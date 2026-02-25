import streamlit as st

from database.db import init_db
from core.state import init_session
from components.navbar import render_navbar
from views import dashboard, roster, payroll, staff, shifts


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="RosMan WMS",
    layout="wide"
)

# --------------------------------------------------
# INIT
# --------------------------------------------------
init_db()
init_session()

if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

# --------------------------------------------------
# LAYOUT STRUCTURE
# --------------------------------------------------

# --- TOP NAV CONTAINER (ALWAYS VISIBLE) ---
nav_container = st.container()
with nav_container:
    render_navbar()

# --- MAIN CONTENT CONTAINER ---
content_container = st.container()

with content_container:
    page = st.session_state["page"]

    if page == "Dashboard":
        dashboard.render()

    elif page == "Roster":
        roster.render()

    elif page == "Payroll":
        payroll.render()

    elif page == "Staff":
        staff.render()

    elif page == "Shifts":
        shifts.render()