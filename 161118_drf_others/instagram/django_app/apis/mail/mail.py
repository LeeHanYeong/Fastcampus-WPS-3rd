from django.core.mail import send_mail as django_send_mail
from django.conf import settings

__all__ = [
    'send_test',
    'send_mail',
]


def send_test():
    django_send_mail('Subject', 'Message', settings.DEFAULT_FROM_EMAIL, ['arcanelux@gmail.com'])


def send_mail(subject, message, recipient_list=None):
    default_recipient_list = ['arcanelux@gmail.com']
    django_send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list if recipient_list else default_recipient_list
    )