import streamlit as st

PAGES = ["Dashboard", "Roster", "Payroll", "Staff", "Shifts"]

def render_navbar():
    col_logo, col_menu, col_user = st.columns([2, 6, 2])

    with col_logo:
        st.markdown("### 🗓 RosMan")

    with col_menu:
        for page in PAGES:
            if st.button(page, key=f"nav_{page}"):
                st.session_state["page"] = page
                st.rerun()

    with col_user:
        st.markdown(f"👤 {st.session_state.get('user', 'Admin')}")

    st.divider()