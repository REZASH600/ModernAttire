from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput({"placeholder": "Email"}), required=False
    )
    subject = forms.CharField(
        max_length=50, widget=forms.TextInput({"placeholder": "Subject"})
    )

    message = forms.CharField(
        widget=forms.Textarea({"placeholder": "Message", "rows": 8})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = self.request.user
        if user.is_authenticated and user.email:
            return user.email

        else:
            if email is None:
                raise ValidationError("Please provide a valid email address.")
            try:
                validate_email(email)
            except ValidationError as e:
                raise ValidationError(e.messages)
        return email
