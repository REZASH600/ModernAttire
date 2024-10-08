from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id", "phone", "username", "is_active", "is_superuser"]
    list_filter = ["is_active", "is_superuser"]
    search_fields = ["phone", "username", "email"]
    list_editable = ["is_active", "is_superuser"]
    ordering = ("phone",)
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("phone", "username", "password"),
            },
        ),
        (
            "Personal Information",
            {
                "fields": ("email", "created_at", "updated_at", "image_file"),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_superuser", "is_verify"),
            },
        ),
        (
            "Group Permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_superuser",
                    "is_verify",
                ),
            },
        ),
    )
