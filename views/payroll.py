import streamlit as st
import pandas as pd
from services.payroll_service import calculate_payroll
from services.email_service import send_payroll_email


def render():
    st.header("Payroll Management")

    payroll = calculate_payroll()

    if not payroll:
        st.info("No payroll data available.")
        return

    df = pd.DataFrame(payroll)
    st.dataframe(df, use_container_width=True)

    st.divider()

    selected_employee = st.selectbox(
        "Send Payroll Email To",
        df["full_name"].tolist()
    )

    if st.button("Send Payroll Email"):
        employee_data = df[df["full_name"] == selected_employee].iloc[0]
        send_payroll_email(employee_data.to_dict())
        st.success(f"Payroll email sent to {selected_employee}.")