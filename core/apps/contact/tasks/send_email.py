from kavenegar import *
from django.conf import settings
from celery import shared_task
from mail_templated import send_mail

api = KavenegarAPI(getattr(settings, "KAVENEGAR_API_KEY"))
DEBUG = getattr(settings, "DEBUG")
EMAIL_HOST_USER = getattr(settings, "EMAIL_HOST_USER")


@shared_task(queue="tasks")
def send_contact_email(subject, message, sender_email):

    context = {"subject": subject, "message": message, "email": sender_email}

    recipient_list = [EMAIL_HOST_USER if EMAIL_HOST_USER else "webmaster@localhost"]

    send_mail(
        template_name="contact/contact_email.tpl",
        context=context,
        from_email=sender_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
