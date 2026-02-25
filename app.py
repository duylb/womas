import streamlit as st

from database.db import init_db
from core.state import init_session
from core.theme import load_theme
from components.navbar import render_navbar

from pages import dashboard, roster, payroll, staff, shifts


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="RosMan WMS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Initialize App
# --------------------------------------------------
init_db()
init_session()
load_theme()

# --------------------------------------------------
# Render Top Navigation
# --------------------------------------------------
render_navbar()

# --------------------------------------------------
# Page Router
# --------------------------------------------------
page = st.session_state.page

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