import apps.accounts.validations
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[apps.accounts.validations.validate_phone],
                        verbose_name="phone",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="username"
                    ),
                ),
                (
                    "image_file",
                    models.ImageField(
                        default="/static/accounts/images/users/user.jpeg",
                        upload_to="images/users",
                        verbose_name="image",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="is active"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="is superuser"),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created date"
                    ),
                ),
                (
                    "updated_date",
                    models.DateTimeField(auto_now=True, verbose_name="updated date"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
    ]
