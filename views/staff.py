import streamlit as st
import pandas as pd


# ==========================================================
# HELPER: Build Unique Key
# ==========================================================
def build_key(full_name, phone, email):
    return (
        full_name.strip().lower(),
        (phone or "").strip(),
        (email or "").strip()
    )


# ==========================================================
# ADD SINGLE STAFF
# ==========================================================
@st.dialog("Add a Staff")
def add_staff_dialog():
    from services.staff_service import add_staff, get_all_staff

    existing_staff = get_all_staff()
    existing_keys = {
        build_key(s.full_name, s.phone, s.email)
        for s in existing_staff
    }

    full_name = st.text_input("Full Name")
    position = st.selectbox("Position", ["Manager", "Service", "Kitchen", "Admin"])
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_input("Address")
    salary_type = st.selectbox("Salary Type", ["hourly", "package"])
    salary_value = st.number_input("Salary Amount", min_value=0.0)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("ADD"):
            new_key = build_key(full_name, phone, email)

            if new_key in existing_keys:
                st.warning("Duplicate staff detected. Ignored.")
                return

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
            st.success("Staff added.")
            st.rerun()

    with col2:
        if st.button("CANCEL"):
            st.rerun()


# ==========================================================
# IMPORT STAFF LIST
# ==========================================================
@st.dialog("Import Staff List (CSV)")
def import_staff_dialog():
    from services.staff_service import add_staff, get_all_staff

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if not uploaded_file:
        return

    try:
        df = pd.read_csv(uploaded_file)

        required_columns = ["full_name", "position", "phone", "email", "address"]
        if not all(col in df.columns for col in required_columns):
            st.error("CSV must contain: full_name, position, phone, email, address")
            return

        existing_staff = get_all_staff()
        existing_keys = {
            build_key(s.full_name, s.phone, s.email)
            for s in existing_staff
        }

        added = 0
        skipped = 0

        for _, row in df.iterrows():
            new_key = build_key(row["full_name"], row["phone"], row["email"])

            if new_key in existing_keys:
                skipped += 1
                continue

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

            # update key set immediately
            existing_keys.add(new_key)
            added += 1

        st.success(f"Imported {added}. Skipped {skipped} duplicates.")
        st.rerun()

    except Exception as e:
        st.error(f"Import failed: {e}")


# ==========================================================
# EDIT STAFF
# ==========================================================
@st.dialog("Edit Staff")
def edit_staff_dialog(staff):
    from services.staff_service import deactivate_staff
    from database.db import SessionLocal
    from database.models import Staff

    full_name = st.text_input("Full Name", value=staff.full_name)

    positions = ["Manager", "Service", "Kitchen", "Admin"]
    default_index = positions.index(staff.position) if staff.position in positions else 0
    position = st.selectbox("Position", positions, index=default_index)

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

            st.success("Updated.")
            st.rerun()

    with col2:
        if st.button("DELETE"):
            deactivate_staff(staff.id)
            st.success("Removed.")
            st.rerun()

    with col3:
        if st.button("CANCEL"):
            st.rerun()


# ==========================================================
# MAIN PAGE
# ==========================================================
def render():
    from services.staff_service import get_all_staff

    st.header("Staff Management")

    col1, col2 = st.columns(2)

    if col1.button("➕ Add a Staff"):
        add_staff_dialog()

    if col2.button("📂 Add Staff List"):
        import_staff_dialog()

    st.divider()

    staff_list = get_all_staff()

    if not staff_list:
        st.info("No active staff.")
        return

    # Display table
    data = []
    for s in staff_list:
        salary = s.hourly_rate if s.salary_type == "hourly" else s.package_salary
        data.append({
            "Full Name": s.full_name,
            "Position": s.position,
            "Phone": s.phone,
            "Email": s.email,
            "Address": s.address,
            "Salary": salary
        })

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Edit selector (replaces row button)
    selected_name = st.selectbox(
        "Select staff to edit",
        [s.full_name for s in staff_list]
    )

    selected_staff = next(s for s in staff_list if s.full_name == selected_name)

    if st.button("Edit Selected Staff"):
        edit_staff_dialog(selected_staff)