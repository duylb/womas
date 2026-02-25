import streamlit as st


def init_session():
    if "user" not in st.session_state:
        st.session_state.user = "Admin"

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"