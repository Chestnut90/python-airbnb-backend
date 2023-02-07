from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    readonly_fields = ("first_name", "last_name")
    fieldsets = (
        (
            "Personal info",
            {
                "classes": ("wide",),
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "email",
                    "gender",
                    "language",
                    "currency",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {
                "classes": ("collapse",),
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

    list_display = ("username", "email", "name", "is_host")
