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
# INITIALIZATION
# --------------------------------------------------
init_db()
init_session()

# Ensure page always exists
if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

# --------------------------------------------------
# NAVBAR (ALWAYS FIRST VISIBLE ELEMENT)
# --------------------------------------------------
render_navbar()

# --------------------------------------------------
# ROUTER
# --------------------------------------------------
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