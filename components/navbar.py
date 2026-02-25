import streamlit as st

def render_navbar():
    col1, col2 = st.columns([6, 2])

    with col1:
        st.markdown("## 🗓 RosMan Workforce Management System")

    with col2:
        st.markdown("👤 Admin")

    st.markdown("---")