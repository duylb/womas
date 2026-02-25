import streamlit as st
from services.staff_service import get_all_staff
from services.payroll_service import calculate_payroll
from services.shift_service import get_all_shifts


def render():
    st.header("Dashboard")

    staff = get_all_staff()
    shifts = get_all_shifts()
    payroll = calculate_payroll()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Staff", len(staff))

    with col2:
        st.metric("Total Shift Types", len(shifts))

    with col3:
        total_payroll = sum(p["total_salary"] for p in payroll) if payroll else 0
        st.metric("Total Payroll", f"{total_payroll:,.0f}")

    st.divider()

    st.subheader("Recent Payroll Overview")

    if payroll:
        for p in payroll:
            st.write(f"**{p['full_name']}** — {p['total_salary']:,.0f}")
    else:
        st.info("No payroll data available.")