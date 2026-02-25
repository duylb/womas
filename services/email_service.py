import smtplib
from email.message import EmailMessage
from config import SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD

def send_payroll_email(to_email, name, hours, salary):
    msg = EmailMessage()
    msg["Subject"] = "Monthly Payroll"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    msg.set_content(f"""
Hello {name},

Your payroll summary:

Total Hours: {hours}
Total Salary: {salary}

Best regards,
Management
""")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)