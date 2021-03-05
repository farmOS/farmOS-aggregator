import logging
from functools import lru_cache
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import emails
import jwt
from emails.template import JinjaTemplate
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.core import config
from app.core.jwt import create_farm_api_token
from app.schemas.farm import FarmBase

password_reset_jwt_subject = "preset"


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()


def send_email(email_to: str, subject_template="", html_template="", environment={}):
    if not settings.EMAILS_ENABLED:
        if settings.EMAIL_TESTING:
            logging.info("\nMessage: " + subject_template + "\nSent to: " + email_to)
            return

        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Emails not enabled."
        )

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


def send_admin_alert_email(email_to: str, message: str):
    aggregator_name = settings.AGGREGATOR_NAME

    subject = f"Admin alert for {aggregator_name}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "admin_alert.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/main/dashboard"

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "aggregator_name": settings.AGGREGATOR_NAME,
            "link": link,
            "message": message,
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


def send_farm_registration_email(email_to: str, link: str):
    aggregator_name = settings.AGGREGATOR_NAME
    subject = f"Register with the {aggregator_name}"

    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "registration_invite.html") as f:
        template_str = f.read()

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "aggregator_name": settings.AGGREGATOR_NAME,
            "link": link,
        },
    )


def send_farm_authorization_email(email_to: str, link: str, farm: FarmBase):
    aggregator_name = settings.AGGREGATOR_NAME
    subject = f"Authorize your farmOS server with the {aggregator_name}"

    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "authorize_email.html") as f:
        template_str = f.read()

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "aggregator_name": settings.AGGREGATOR_NAME,
            "link": link,
            "farm": FarmBase,
        },
    )


def generate_farm_authorization_link(farm_id):
    token = create_farm_api_token(farm_id=[farm_id], scopes=["farm:read", "farm:authorize", "farm.info"])

    server_host = settings.SERVER_HOST
    link = f"{server_host}/authorize-farm/?farm_id={farm_id}&api_token={token.decode()}"

    return link


def generate_farm_registration_link():
    token = create_farm_api_token(farm_id=[], scopes=["farm:create", "farm:info"])

    server_host = settings.SERVER_HOST
    link = f"{server_host}/authorize-farm?api_token={token.decode()}"

    return link
