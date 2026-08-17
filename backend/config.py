from dotenv import load_dotenv
import os

ENV = os.getenv("ENV", "development")

if ENV == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

DATABASE_URL=os.getenv("DATABASE_URL")

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))

MAIL_STARTTLS = os.getenv("MAIL_STARTTLS") == "True"
MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS") == "True"

FRONTEND_URL = os.getenv("FRONTEND_URL")

EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS = int(
    os.getenv("EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS")
)

PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_MINUTES")
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
)