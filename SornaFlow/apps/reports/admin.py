from .models import Reports
from django.contrib import admin
from django.utils.html import format_html


class ReportsReadOnlyInline(admin.TabularInline):
    """
    Inline for displaying related reports in read‑only mode
    inside the task edit page.
    """
    model = Reports

    # Fields shown in the inline table
    fields = ('employee', 'description', 'display_status',
              'file_preview_inline', "created_at")

    # Fields that cannot be edited
    readonly_fields = ('employee', 'description', 'display_status',
                       'file_preview_inline', "created_at")

    def display_status(self, obj):
        """Return human‑readable status label."""
        return obj.get_status_display()
    display_status.short_description = 'وضعیت'

    def file_preview_inline(self, obj):
        """
        Show a small preview for image files,
        otherwise show a download link.
        """
        if obj.file_upload_reports:
            if obj.file_upload_reports.name.lower().endswith(
                ('.png', '.jpg', '.jpeg', '.gif')
            ):
                return format_html(
                    '<a href="{}" target="_blank">'
                    '<img src="{}" width="50" height="50" style="object-fit: cover;"/>'
                    '</a>',
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
        """Disable adding new reports from inline."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deleting reports from inline."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing reports from inline."""
        return False
