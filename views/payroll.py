import streamlit as st
import pandas as pd
from datetime import datetime


def render():
    from services.payroll_service import calculate_monthly_payroll
    from services.email_service import send_payroll_email

    st.header("Payroll Management")

    today = datetime.today()
    payroll = calculate_monthly_payroll(today.month, today.year)

    if not payroll:
        st.info("No payroll data available.")
        return

    df = pd.DataFrame(payroll)
    st.dataframe(df, use_container_width=True)

    st.divider()

    selected = st.selectbox("Send Payroll Email To", df["name"].tolist())

    if st.button("Send Email"):
        employee_data = df[df["name"] == selected].iloc[0].to_dict()
        send_payroll_email(employee_data)
        st.success("Payroll email sent.")