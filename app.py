import streamlit as st

from database.db import init_db
from core.state import init_session
from core.theme import load_theme
from components.navbar import render_navbar

from views import dashboard, roster, payroll, staff, shifts


st.set_page_config(
    page_title="RosMan WMS",
    layout="wide"
)

init_db()
init_session()
# load_theme()

# Ensure page always exists
if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

# Render navbar
render_navbar()
st.write("NAVBAR RENDERED")
# Route pages
page = st.session_state.get("page")

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