from django.contrib.auth import password_validation
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from . import validations

from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import random


class MyUserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, phone, username, password, **extra_fields):
        """
        Create and return a user with the specified phone, username,
        and password.

        Raises ValueError if any required fields are missing or if
        the password fails validation.

        Returns:
            User: The created user instance.
        """
        if not phone:
            raise ValueError("The Phone field must be set.")

        if not username:
            raise ValueError("The Username field must be set.")

        if not password:
            raise ValueError("The password field must be set.")

        user = self.model(phone=phone, username=username, **extra_fields)

        if "email" in extra_fields:
            user.email = self.normalize_email(extra_fields["email"])

        try:
            password_validation.validate_password(password=password)
        except ValidationError as e:
            raise ValueError(f"Password validation error: {', '.join(e.messages)}.")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password=None, **extra_fields):
        """
        Create and return a superuser with the specified phone,
        username, and password.

        Ensures the superuser is marked as active and has superuser
        permissions.

        Raises ValueError if is_superuser or is_active are not True.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True."))

        return self.create_user(phone, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        _("phone"), max_length=11, unique=True, validators=[validations.validate_phone]
    )
    email = models.EmailField(_("email address"), max_length=255, null=True, blank=True)
    username = models.CharField(_("username"), max_length=255, unique=True)
    image_file = models.ImageField(
        _("image"),
        default="images/users/user.jpeg",
        upload_to="images/users",
    )

    is_active = models.BooleanField(_("is active"), default=True)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    is_verify = models.BooleanField(_("is verify"), default=False)
    
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.phone

    def clean(self):
        """
        Validates the email field to ensure it is unique.

        Raises a ValidationError if the email is already in use by another user,
        excluding the current user being updated.

        Returns:
            None
        """
        email = self.email
        if email:
            if User.objects.filter(email=email).exclude(pk=self.pk).exists():
                raise ValidationError(_("This email is already in use."))
        super().clean()

    @property
    def is_staff(self):
        """Returns True if the user is active and a superuser."""
        return self.is_active and self.is_superuser

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Otp(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user"), related_name="otp"
    )
    code = models.CharField(_("code"), max_length=6)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    expires_at = models.DateTimeField(_("expires at"))

    def save(self, *args, **kwargs):

        if not self.expires_at:
            expiration_minutes = getattr(settings, "OTP_EXPIRATION_TIME", 5)
            self.expires_at = timezone.now() + timedelta(minutes=expiration_minutes)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def get_active_otp(cls, user_id, code=None):
        """
        Retrieve the active OTP for a specified user.

        Parameters:
            user_id (int): The ID of the user.
            code (str, optional): The specific OTP code to match.

        Returns:
            Otp or None: The active OTP instance if found and not expired; otherwise, None.
        """

        otp = Otp.objects.filter(
            Q(user_id=user_id) & (Q(code=code) if code else Q())
        ).first()
        if otp:
            if not otp.is_expired:
                return otp

        return None
    
    @classmethod
    def create_otp_for_user(cls,user_id):
        """Create an OTP for a specific user."""
        
        code = random.randint(100000,999999)
        return Otp.objects.create(user_id=user_id,code=code)

    def __str__(self):
        return f"OTP for {self.user}: {self.code} (Expires at: {self.expires_at})"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("One Time Password")
        verbose_name_plural = _("One Time Passwords")
