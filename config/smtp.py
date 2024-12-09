import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from dotenv import dotenv_values

config = dotenv_values(".env")

email_conf = ConnectionConfig(
    MAIL_USERNAME=config['MAIL_USERNAME'],
    MAIL_PASSWORD=config['MAIL_PASSWORD'],
    MAIL_FROM=config['MAIL_FROM'],
    MAIL_PORT=config['MAIL_PORT'],
    MAIL_SERVER=config['MAIL_SERVER'],
    MAIL_FROM_NAME=config['MAIL_FROM_NAME'],
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def verification_code_email(subject: str, email_to: list, code: int):
    html = f"""<p>Welcome to AquaAlaga!</p>
        <p>Verification Code: {code}</p>"""
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        body=html,
        subtype=MessageType.html)
    
    fm = FastMail(email_conf)
    result = await fm.send_message(message)
    print(result)
    return True

async def reset_code_email(subject: str, email_to: list, code: int):
    html = f"""<p>Hello, use this code to reset your password.</p>
        <p>Reset Code: {code}</p>"""
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        body=html,
        subtype=MessageType.html)
    
    fm = FastMail(email_conf)
    result = await fm.send_message(message)
    print(result)
    return True