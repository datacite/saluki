from saluki.config import settings
import httpx

from saluki.dependencies.security import create_verification_token
from saluki.models import DBUser
from saluki.routers.users import user_router

CONFIRMATION_EMAIL_TEMPLATE = """
Dear {name},

Welcome to the DataCite Data Files Service.
Please click the link below to confirm your email address and activate your account:
{confirmation_url}

Thanks,

The DataCite Support Team


DataCite
Am Welfengarten 1B
30167 Hannover
Germany
Email: support@datacite.org
"""


def send_email(to: str, subject: str, body: str) -> dict:
    print(settings.mailgun_api_key)
    response = httpx.post(
        f"{settings.mailgun_endpoint}/messages",
        auth=("api", settings.mailgun_api_key),
        data={
            "from": f"{settings.email_from} <{settings.email_address}>",
            "to": to,
            "subject": subject,
            "text": body,
        },
    )
    response.raise_for_status()
    return response.json()


def send_confirmation_email(user: DBUser) -> dict:
    confirmation_token = create_verification_token(user)
    confirmation_url = user_router.url_path_for("confirm_user", token=confirmation_token)
    body = CONFIRMATION_EMAIL_TEMPLATE.format(
        name=user.name, confirmation_url=confirmation_url
    )
    return send_email(user.email, "Confirm your email address", body)
