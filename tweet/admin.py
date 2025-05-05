from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tweet, CustomUser

# Register your models here.
admin.site.register(Tweet)

# Register the CustomUser model with the admin panel
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("sap_id",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("sap_id",)}),
    )