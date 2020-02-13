import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import emails
import jwt
from emails.template import JinjaTemplate
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.jwt import create_farm_api_token

password_reset_jwt_subject = "preset"


def send_email(email_to: str, subject_template="", html_template="", environment={}):
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str):
    aggregator_name = settings.AGGREGATOR_NAME
    subject = f"{aggregator_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"aggregator_name": settings.AGGREGATOR_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str):
    aggregator_name = settings.AGGREGATOR_NAME
    subject = f"{aggregator_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={use_token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "aggregator_name": settings.AGGREGATOR_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str):
    aggregator_name = settings.AGGREGATOR_NAME
    subject = f"{aggregator_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "aggregator_name": settings.AGGREGATOR_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email):
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": password_reset_jwt_subject, "email": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except InvalidTokenError:
        return None


def generate_farm_authorization_link(farm_id):
    token = create_farm_api_token(farm_id=[farm_id], scopes=["farm:read", "farm:authorize", "farm.info"])

    server_host = settings.SERVER_HOST
    api_path = settings.API_V1_STR
    link = f"{server_host}/authorize-farm/?farm_id={farm_id}&api_token={token.decode()}"

    return link


def generate_farm_registration_link():
    token = create_farm_api_token(farm_id=[], scopes=["farm:create", "farm:info"])

    server_host = settings.SERVER_HOST
    api_path = settings.API_V1_STR
    link = f"{server_host}/register-farm?api_token={token.decode()}"

    return link
