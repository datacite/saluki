from saluki.config import settings
import httpx


def send_email(to, subject, body):
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
