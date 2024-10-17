{% extends "mail_templated/base.tpl" %}

{% block subject %}
    New Contact from {{ email }}
{% endblock %}

{% block html %}
    <div style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; padding: 20px; margin: 0;">
        <div style="background: #fff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <h1 style="color: #333;">New Contact from {{ email }}</h1>
            <p><strong>Subject:</strong> {{ subject }}</p>
            <p><strong>Message:</strong></p>
            <p>{{ message }}</p>

            <p>Thank you for your attention.</p>
            <p>Best regards,</p>
            <p>Your Support Team</p>
        </div>
    </div>
{% endblock %}
