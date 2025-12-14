from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmployeeUser
from .forms import EmployeeUserChangeForm, EmployeeUserCreationForm
from django.utils.safestring import mark_safe

class CustomUserAdmin(UserAdmin):
    form = EmployeeUserChangeForm
    add_form = EmployeeUserCreationForm
    list_display = ('national_code', 'email',"mobile_number", "name", "family","father_name","birth_date","certificate","marital_status", "photo_preview", "gender","employee_address", "is_active", "is_admin")
    list_filter = ("is_active", "is_admin",)
    

    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('national_code', 'password',"mobile_number")}),
        ('اطلاعات شخصی', {"fields": ("email", 'name', "family","father_name","gender", "birth_date","certificate","marital_status","employee_address","image", "company")}),
        ('دسترسی‌ها', {"fields": ("is_active", "is_admin", "is_superuser", 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {'fields': ('national_code',"mobile_number", 'email', "name", "family", "gender" ,'password1', 'password2',"is_active")}),
    )
    
    # اضافه کردن فیلدهای فقط خواندنی
    readonly_fields = ("photo_preview",)  # مهم: اضافه کردن این خط
    
    search_fields = ('national_code',)
    ordering = ('national_code',)
    filter_horizontal = ('groups', 'user_permissions')
    
    def photo_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "بدون عکس"
    
    photo_preview.short_description = "عکس پرسنلی"

admin.site.register(EmployeeUser, CustomUserAdmin)