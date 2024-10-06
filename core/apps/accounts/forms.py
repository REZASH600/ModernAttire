from django import forms
from django.contrib.auth import get_user_model, login, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.core.validators import validate_email
from django.contrib.auth import update_session_auth_hash
from . import validations

User = get_user_model()


class ProfileForm(forms.ModelForm):

    old_password = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "current password"}), required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "new password"}), required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "confirm password"}), required=False
    )

    class Meta:
        model = User
        fields = ["username", "email", "image_file"]

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        old_password = cleaned_data.get("old_password")
        user = self.instance

        # Password change logic
        if new_password or confirm_password:
            # Ensure old password is provided
            if not old_password:
                raise ValidationError(
                    "Please enter your current password to change your password."
                )

            # Verify the old password
            if not user.check_password(old_password):
                raise ValidationError("The current password is incorrect.")

            # Ensure new passwords match
            if new_password != confirm_password:
                raise ValidationError("The new passwords do not match.")

            # Validate the new password according to Django's standards
            try:
                password_validation.validate_password(new_password, user=user)
            except ValidationError as e:
                raise ValidationError(e.messages)

        return super().clean()    

    def save(self, commit=True, request=None):
        user = super().save(commit=False)

        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

            if request:
                update_session_auth_hash(request, user)

        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(
        max_length=255, widget=forms.TextInput({"placeholder": "phone or email"})
    )
    password = forms.CharField(widget=forms.PasswordInput({"placeholder": "password"}))

    def clean_identifier(self):
        identifier = self.cleaned_data.get("identifier")

        if not identifier:
            raise ValidationError(
                "Identifier must be a valid phone number or email address."
            )

        elif identifier.isdigit():
            try:
                validations.validate_phone(identifier)
            except ValidationError as e:
                raise ValidationError(e.messages)

        elif "@" in identifier:
            try:
                validate_email(identifier)
            except ValidationError as e:
                raise ValidationError(e.messages)

        return identifier