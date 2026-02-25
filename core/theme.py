import streamlit as st

def load_theme():
    st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    </style>
    """, unsafe_allow_html=True)