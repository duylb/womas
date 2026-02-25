import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///rosman.db")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "yourcompany@email.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "APP_PASSWORD")