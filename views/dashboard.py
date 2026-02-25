import streamlit as st
from datetime import datetime

def render():
    from services.staff_service import get_all_staff
    from services.payroll_service import calculate_monthly_payroll
    from services.shift_service import get_shifts

    st.header("Dashboard")

    staff = get_all_staff()
    shifts = get_shifts()

    today = datetime.today()
    payroll = calculate_monthly_payroll(today.month, today.year)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Staff", len(staff))

    with col2:
        st.metric("Total Shift Types", len(shifts))

    with col3:
        total_payroll = sum(p["salary"] for p in payroll) if payroll else 0
        st.metric("Total Payroll", f"{total_payroll:,.0f}")

    st.divider()

    if payroll:
        st.subheader("Current Month Payroll")
        for p in payroll:
            st.write(f"**{p['name']}** — {p['salary']:,.0f}")
    else:
        st.info("No payroll data available.")