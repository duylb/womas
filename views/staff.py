import streamlit as st


def render():
    from services.staff_service import (
        get_all_staff,
        add_staff,
        deactivate_staff
    )

    st.header("Staff Management")

    # ------------------------
    # Add Staff
    # ------------------------
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
            staff_data = {
                "full_name": full_name,
                "position": position,
                "salary_type": salary_type,
                "hourly_rate": salary_value if salary_type == "hourly" else None,
                "package_salary": salary_value if salary_type == "package" else None,
                "phone": phone,
                "email": email,
                "is_active": True
            }

            add_staff(staff_data)
            st.success("Staff added successfully.")
            st.rerun()

    st.divider()

    # ------------------------
    # Staff List
    # ------------------------
    st.subheader("Active Staff")

    staff_list = get_all_staff()

    if not staff_list:
        st.info("No staff available.")
        return

    for staff in staff_list:
        col1, col2 = st.columns([8, 1])

        with col1:
            st.write(f"**{staff.full_name}** — {staff.position}")

        with col2:
            if st.button("Deactivate", key=f"deactivate_{staff.id}"):
                deactivate_staff(staff.id)
                st.success("Staff deactivated.")
                st.rerun()