import streamlit as st
from database.db import init_db
from core.theme import load_theme
from core.state import init_session
from components.navbar import render_navbar

from pages import dashboard, roster, payroll, staff, shifts

st.set_page_config(page_title="RosMan WMS", layout="wide")

init_db()
init_session()
load_theme()
render_navbar()

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Roster", "Payroll", "Staff", "Shifts"]
)

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