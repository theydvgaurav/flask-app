import os
from datetime import datetime, timedelta
from random import randint

from celery import shared_task

from utils.mailer import EmailWrapper


def generate_otp_with_expiry(otp_length: int, expires_in_min: int = 10):
    otp_code = _random_with_n_digits(otp_length)
    expires_at = datetime.utcnow() + timedelta(minutes=expires_in_min)
    return otp_code, expires_at


def _random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def get_mailer_instance():
    smtp_server = 'smtp.gmail.com'
    port = 587
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    return EmailWrapper(smtp_server=smtp_server, port=port, username=username, password=password)


def send_otp_email(to_address, otp_code):
    mailer_instance = get_mailer_instance()
    subject = 'Your Login OTP'
    body = f'Use {otp_code} to login into your account. This Otp expires in 15 minutes.'
    mailer_instance.send_email(to_address, subject, body, os.getenv("SMTP_USERNAME"))
