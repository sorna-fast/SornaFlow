from .models import Reports
from django.contrib import admin
from django.utils.html import format_html


class ReportsReadOnlyInline(admin.TabularInline):
    """
    این کلاس گزارش‌های مرتبط با یک وظیفه را به صورت فقط-خواندنی
    در صفحه ویرایش وظایف نمایش می‌دهد.
    """
    model = Reports
    
    #  تغییر اصلی: به جای 'status' از 'display_status' استفاده می‌کنیم
    fields = ('employee', 'description', 'display_status', 'file_preview_inline',"created_at")
    readonly_fields = ('employee', 'description', 'display_status', 'file_preview_inline',"created_at") 

    #  این متد جدید را برای نمایش وضعیت اضافه کنید
    def display_status(self, obj):
        return obj.get_status_display()
    # این خط، عنوان ستون در پنل ادمین را تنظیم می‌کند
    display_status.short_description = 'وضعیت'

    # متدی برای نمایش پیش‌نمایش فایل در حالت Inline
    def file_preview_inline(self, obj):
        if obj.file_upload_reports:
            if obj.file_upload_reports.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html(
                    '<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover;"/></a>',
                    obj.file_upload_reports.url,
                    obj.file_upload_reports.url
                )
            return format_html(
                '<a href="{}" download>دانلود فایل</a>',
                obj.file_upload_reports.url
            )
        return "بدون فایل"
    file_preview_inline.short_description = 'فایل ضمیمه'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
