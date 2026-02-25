import streamlit as st
from services.staff_service import get_all_staff, add_staff, deactivate_staff

def render():
    st.title("Staff Management")

    with st.form("add_staff"):
        st.subheader("Add Staff")

        name = st.text_input("Full Name")
        position = st.text_input("Position")
        salary_type = st.selectbox("Salary Type", ["hourly","package"])
        hourly = st.number_input("Hourly Rate", 0.0)
        package = st.number_input("Package Salary", 0.0)
        phone = st.text_input("Phone")
        email = st.text_input("Email")

        if st.form_submit_button("Add"):
            add_staff({
                "full_name": name,
                "position": position,
                "salary_type": salary_type,
                "hourly_rate": hourly,
                "package_salary": package,
                "phone": phone,
                "email": email
            })
            st.success("Staff added")

    st.subheader("Active Staff")

    staff = get_all_staff()
    for s in staff:
        col1, col2 = st.columns([4,1])
        col1.write(f"{s.full_name} - {s.position}")
        if col2.button("Remove", key=s.id):
            deactivate_staff(s.id)
            st.rerun()