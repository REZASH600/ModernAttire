from kavenegar import *
from django.conf import settings
from celery import shared_task
from mail_templated import send_mail
from django.template.loader import render_to_string

api = KavenegarAPI(getattr(settings, "KAVENEGAR_API_KEY"))
sender = getattr(settings, "KAVENEGAR_SENDER")
DEBUG = getattr(settings, "DEBUG")
EMAIL_HOST_USER = getattr(settings, "EMAIL_HOST_USER")


@shared_task(queue="tasks")
def send_otp_sms(username, phone, code):

    if DEBUG:
        print(code)

    params = {
        "sender": sender,
        "receptor": phone,
        "message": f"Hello {username}, your verification code is: {code}.",
    }
    try:
        response = api.sms_send(params)
        return response

    except APIException as e:
        # Catch and handle API exceptions
        print(f"API Error: {e}")
        raise

    except HTTPException as e:
        # Catch and handle HTTP exceptions
        print(f"HTTP Error: {e}")
        raise

    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise


@shared_task(queue="tasks")
def send_otp_email(username, email, code):

    context = {"username": username, "otp_code": code}

    send_mail(
        template_name="accounts/otp_email.tpl",
        context=context,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
