import streamlit as st
from services.payroll_service import calculate_monthly_payroll
from services.email_service import send_payroll_email
from datetime import datetime

def render():
    st.title("Payroll")

    month = st.number_input("Month", 1, 12, datetime.now().month)
    year = st.number_input("Year", 2020, 2100, datetime.now().year)

    if st.button("Calculate Payroll"):
        payroll = calculate_monthly_payroll(month, year)

        for p in payroll:
            st.write(p)

            if st.button(f"Send Email to {p['name']}", key=p['name']):
                send_payroll_email(
                    p["email"],
                    p["name"],
                    p["total_hours"],
                    p["salary"]
                )
                st.success("Email sent")