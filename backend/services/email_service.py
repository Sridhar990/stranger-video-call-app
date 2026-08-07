from fastapi_mail import ConnectionConfig,FastMail,MessageSchema,MessageType
from config import (
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_FROM,
    MAIL_SERVER,
    MAIL_PORT,
    MAIL_STARTTLS,
    MAIL_SSL_TLS,
)

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_PORT=MAIL_PORT,
    MAIL_STARTTLS=MAIL_STARTTLS,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
)


async def send_verification_email(
        email:str,
        username:str,
        verification_link:str
):
    message = MessageSchema(
        subject= "Verify Your Email",
        recipients= [email],
        body=f"""
Hello {username},
Welcome to Stranger Video Call.

Click the link below to verify your email:
{verification_link}

If you did not create this account, please ignore this email.

Thank you.

""",
subtype= MessageType.plain

    )

    fm=FastMail(conf)
    await fm.send_message(message)