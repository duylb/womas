import streamlit as st


def load_theme():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0f172a;
            color: #e5e7eb;
        }

        section[data-testid="stSidebar"] {
            display: none;
        }

        .block-container {
            padding-top: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        div[data-testid="metric-container"] {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 12px;
            border-radius: 12px;
        }
        </style>
    """, unsafe_allow_html=True)