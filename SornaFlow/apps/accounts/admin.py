from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmployeeUser
from .forms import EmployeeUserChangeForm, EmployeeUserCreationForm
from django.utils.safestring import mark_safe

class CustomUserAdmin(UserAdmin):
    form = EmployeeUserChangeForm  # Form used for editing existing users
    add_form = EmployeeUserCreationForm  # Form used for creating new users

    # Fields displayed in the admin list view
    list_display = (
        'national_code', 'email', "mobile_number", "name", "family",
        "father_name", "birth_date", "certificate", "marital_status",
        "photo_preview", "gender", "employee_address",
        "is_active", "is_admin"
    )

    # Filters shown in the right sidebar
    list_filter = ("is_active", "is_admin",)

    # Field groups for editing user details
    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('national_code', 'password', "mobile_number")}),
        ('اطلاعات شخصی', {
            "fields": (
                "email", 'name', "family", "father_name", "gender",
                "birth_date", "certificate", "marital_status",
                "employee_address", "image", "company"
            )
        }),
        ('دسترسی‌ها', {
            "fields": (
                "is_active", "is_admin", "is_superuser",
                'groups', 'user_permissions'
            )
        }),
    )

    # Field groups for creating a new user
    add_fieldsets = (
        (None, {
            'fields': (
                'national_code', "mobile_number", 'email', "name",
                "family", "gender", 'password1', 'password2', "is_active"
            )
        }),
    )

    readonly_fields = ("photo_preview",)  # Makes preview image non-editable

    search_fields = ('national_code',)  # Enables search by national code
    ordering = ('national_code',)  # Default ordering in admin list
    filter_horizontal = ('groups', 'user_permissions')  # Better UI for M2M fields

    def photo_preview(self, obj):
        # Returns an HTML image tag for previewing the user's photo
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "بدون عکس"  # Fallback text when no image exists

    photo_preview.short_description = "عکس پرسنلی"  # Label shown in admin UI

# Registers the custom admin configuration for EmployeeUser
admin.site.register(EmployeeUser, CustomUserAdmin)
