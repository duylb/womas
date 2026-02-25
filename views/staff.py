import streamlit as st
import pandas as pd


# ==========================================================
# ADD SINGLE STAFF DIALOG
# ==========================================================
@st.dialog("Add a Staff")
def add_staff_dialog():
    from services.staff_service import add_staff

    full_name = st.text_input("Full Name")
    position = st.selectbox(
        "Position",
        ["Manager", "Service", "Kitchen", "Admin"]
    )
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_input("Address")

    salary_type = st.selectbox("Salary Type", ["hourly", "package"])
    salary_value = st.number_input("Salary Amount", min_value=0.0)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("ADD"):
            staff_data = {
                "full_name": full_name,
                "position": position,
                "phone": phone,
                "email": email,
                "address": address,
                "salary_type": salary_type,
                "hourly_rate": salary_value if salary_type == "hourly" else None,
                "package_salary": salary_value if salary_type == "package" else None,
                "is_active": True
            }

            add_staff(staff_data)
            st.success("Staff added successfully.")
            st.rerun()

    with col2:
        if st.button("CANCEL"):
            st.rerun()


# ==========================================================
# IMPORT STAFF LIST DIALOG
# ==========================================================
@st.dialog("Import Staff List (CSV)")
def import_staff_dialog():
    from services.staff_service import add_staff

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            required_columns = ["full_name", "position", "phone", "email", "address"]

            if not all(col in df.columns for col in required_columns):
                st.error(
                    "CSV must contain columns: full_name, position, phone, email, address"
                )
                return

            for _, row in df.iterrows():
                staff_data = {
                    "full_name": row["full_name"],
                    "position": row["position"],
                    "phone": row["phone"],
                    "email": row["email"],
                    "address": row["address"],
                    "salary_type": "hourly",
                    "hourly_rate": 0,
                    "package_salary": None,
                    "is_active": True
                }
                add_staff(staff_data)

            st.success("Staff list imported successfully.")
            st.rerun()

        except Exception as e:
            st.error(f"Import failed: {e}")


# ==========================================================
# EDIT STAFF DIALOG
# ==========================================================
@st.dialog("Edit Staff")
def edit_staff_dialog(staff):
    from services.staff_service import deactivate_staff
    from database.db import SessionLocal
    from database.models import Staff

    full_name = st.text_input("Full Name", value=staff.full_name)

    # SAFE POSITION HANDLING
    positions = ["Manager", "Service", "Kitchen", "Admin"]
    normalized_positions = [p.lower() for p in positions]

    if staff.position and staff.position.lower() in normalized_positions:
        default_index = normalized_positions.index(staff.position.lower())
    else:
        default_index = 0

    position = st.selectbox(
        "Position",
        positions,
        index=default_index
    )

    phone = st.text_input("Phone", value=staff.phone or "")
    email = st.text_input("Email", value=staff.email or "")
    address = st.text_input("Address", value=staff.address or "")

    salary_type = st.selectbox(
        "Salary Type",
        ["hourly", "package"],
        index=0 if staff.salary_type == "hourly" else 1
    )

    salary_value = st.number_input(
        "Salary Amount",
        value=float(staff.hourly_rate or staff.package_salary or 0),
        min_value=0.0
    )

    col1, col2, col3 = st.columns(3)

    # SAVE
    with col1:
        if st.button("SAVE"):
            db = SessionLocal()
            db_staff = db.query(Staff).get(staff.id)

            db_staff.full_name = full_name
            db_staff.position = position
            db_staff.phone = phone
            db_staff.email = email
            db_staff.address = address
            db_staff.salary_type = salary_type
            db_staff.hourly_rate = salary_value if salary_type == "hourly" else None
            db_staff.package_salary = salary_value if salary_type == "package" else None

            db.commit()
            db.close()

            st.success("Staff updated successfully.")
            st.rerun()

    # DELETE (Deactivate)
    with col2:
        if st.button("DELETE"):
            deactivate_staff(staff.id)
            st.success("Staff deactivated.")
            st.rerun()

    # CANCEL
    with col3:
        if st.button("CANCEL"):
            st.rerun()


# ==========================================================
# MAIN STAFF PAGE
# ==========================================================
def render():
    from services.staff_service import get_all_staff

    st.header("Staff Management")

    # Action Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add a Staff"):
            add_staff_dialog()

    with col2:
        if st.button("📂 Add Staff List"):
            import_staff_dialog()

    st.divider()

    # Staff List
    staff_list = get_all_staff()

    if not staff_list:
        st.info("No active staff available.")
        return

    st.subheader("Current Staff")

    for staff in staff_list:
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 3, 3, 1])

        col1.write(staff.full_name)
        col2.write(staff.position)
        col3.write(staff.phone or "")
        col4.write(staff.email or "")
        col5.write(staff.address or "")

        if col6.button("Edit", key=f"edit_{staff.id}"):
            edit_staff_dialog(staff)