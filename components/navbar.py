import streamlit as st

PAGES = ["Dashboard", "Roster", "Payroll", "Staff", "Shifts"]


def render_navbar():
    st.markdown("""
        <style>
        .navbar {
            background-color: #0f172a;
            padding: 14px 30px;
            border-bottom: 1px solid #1f2937;
        }

        .nav-button button {
            background: none !important;
            border: none !important;
            color: #e5e7eb !important;
            font-weight: 500 !important;
        }

        .nav-button button:hover {
            color: #3b82f6 !important;
        }

        .active-page button {
            color: #3b82f6 !important;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col_logo, col_menu, col_user = st.columns([2, 7, 2])

    # Logo
    with col_logo:
        st.markdown("### 🗓 RosMan")

    # Navigation Menu
    with col_menu:
        menu_cols = st.columns(len(PAGES))

        for i, page in enumerate(PAGES):
            is_active = st.session_state.page == page

            container = menu_cols[i].container()

            with container:
                if is_active:
                    st.markdown('<div class="active-page nav-button">', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="nav-button">', unsafe_allow_html=True)

                if st.button(page, key=f"nav_{page}", use_container_width=True):
                    st.session_state.page = page
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    # User Info
    with col_user:
        st.markdown(f"👤 {st.session_state.user}")

    st.markdown("---")