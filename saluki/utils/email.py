from saluki.config import settings
import httpx


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


def send_confirmation_email(user, confirmation_url: str) -> dict:

    body = CONFIRMATION_EMAIL_TEMPLATE.format(
        name=user.name, confirmation_url=confirmation_url
    )
    return send_email(user.email, "Confirm your email address", body)
