import os

from celery import shared_task

from apps.users.utils import get_mailer_instance


@shared_task
def send_policy_creation_email(policy):
    if policy:
        mailer_instance = get_mailer_instance()
        subject = 'Health Policy is Created'
        body = (f'Hi {policy.get("customer_name")}!\nYour health policy is created.\nPolicy Number - '
                f'{policy.get("policy_number")}')
        mailer_instance.send_email(policy.get("email"), subject, body, os.getenv("SMTP_USERNAME"))
