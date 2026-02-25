import streamlit as st


def render():
    from services.staff_service import (
        get_all_staff,
        add_staff,
        delete_staff
    )

    st.header("Staff Management")

    st.subheader("Add New Staff")

    with st.form("add_staff_form"):
        full_name = st.text_input("Full Name")
        position = st.text_input("Position")
        salary_type = st.selectbox("Salary Type", ["hourly", "package"])
        salary_value = st.number_input("Salary Amount", min_value=0.0)
        phone = st.text_input("Phone")
        email = st.text_input("Email")

        submitted = st.form_submit_button("Add Staff")

        if submitted:
            add_staff(
                full_name=full_name,
                position=position,
                salary_type=salary_type,
                salary_value=salary_value,
                phone=phone,
                email=email
            )
            st.success("Staff added.")

    st.divider()

    staff_list = get_all_staff()

    for s in staff_list:
        col1, col2 = st.columns([8, 1])

        with col1:
            st.write(f"**{s.full_name}** — {s.position}")

        with col2:
            if st.button("❌", key=f"delete_{s.id}"):
                delete_staff(s.id)
                st.rerun()