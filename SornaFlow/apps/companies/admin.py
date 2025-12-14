from django.contrib import admin
from .models import Company
from django.utils.safestring import mark_safe

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # تنظیمات نمایش لیست
    list_display = ['name', 'address_company', 'phone', 'logo_preview']
    search_fields = ['name', 'address_company', 'phone']
    list_filter = ['name']
    
    # نمایش لوگو در لیست
    readonly_fields = ['logo_preview']
    
    # گروه‌بندی فیلدها در فرم ویرایش
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'address_company', 'phone')
        }),
        ('لوگو', {
            'fields': ('logo', 'logo_preview'),
            'classes': ('collapse',)  # قابل جمع شدن
        }),
    )
    
    # تابع برای نمایش پیش‌نمایش لوگو
    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="100" />')
        return "بدون لوگو"
    
    logo_preview.short_description = "پیش‌نمایش لوگو"