import streamlit as st

PAGES = ["Dashboard", "Roster", "Payroll", "Staff", "Shifts"]

def render_navbar():
    st.markdown("### 🗓 RosMan WMS")

    cols = st.columns(len(PAGES))

    for i, page in enumerate(PAGES):
        if cols[i].button(page, key=f"nav_{page}", use_container_width=True):
            st.session_state["page"] = page
            st.rerun()

    st.divider()