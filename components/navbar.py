import streamlit as st

PAGES = ["Dashboard", "Roster", "Payroll", "Staff", "Shifts"]

def render_navbar():
    st.write("🚀 NAVBAR IS HERE")
    col1, col2 = st.columns([2, 8])

    with col1:
        st.markdown("## 🗓 RosMan")

    with col2:
        nav_cols = st.columns(len(PAGES))

        for i, page in enumerate(PAGES):
            if nav_cols[i].button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state["page"] = page
                st.rerun()

    st.markdown("---")