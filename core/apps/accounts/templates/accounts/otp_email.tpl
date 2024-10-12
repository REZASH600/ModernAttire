{% extends "mail_templated/base.tpl" %}

{% block subject %}
Important: Your OTP Code, {{ username }}!
{% endblock %}

{% block html %}
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd;">
    <h2 style="color: #333;">Hello, {{ username }}!</h2>
    <p style="font-size: 16px; color: #555;">
        We're sending you your OTP code to verify your account.
    </p>
    <p style="font-size: 18px; color: #000;">
        Your OTP code is: <strong>{{ otp_code }}</strong>
    </p>
    <p style="font-size: 14px; color: #777;">
        If you didn't request this code, please disregard this email.
    </p>
</div>
{% endblock %}
