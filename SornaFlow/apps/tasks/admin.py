from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Tasks
from apps.reports.admin import ReportsReadOnlyInline


@admin.register(Tasks)  # Cleaner way to register the admin class
class TasksAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'truncated_description', 'display_employees',
        "is_active", "created_at"
    )  # Columns shown in the admin list view

    search_fields = (
        'title', 'description', 'employees__name',
        'employees__family', "is_active"
    )  # Enable searching by task fields and employee names

    list_per_page = 15  # Pagination size
    inlines = [ReportsReadOnlyInline]  # Show related reports inline

    filter_horizontal = ('employees',)  # Better UI for many‑to‑many employee selection

    def truncated_description(self, obj):
        """Return a shortened version of the task description."""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "بدون توضیحات"
    truncated_description.short_description = 'توضیحات مختصر'

    def display_employees(self, obj):
        """
        Display related employees as clickable admin links.
        """
        employees = obj.employees.all()
        if not employees:
            return "بدون کارمند"

        links = []
        for emp in employees:
            url = reverse('admin:accounts_employeeuser_change', args=[emp.pk])  # Admin edit link
            links.append(f'<a href="{url}" target="_blank">{emp.name} {emp.family}</a>')

        html = "<br>".join(links)
        return format_html(html) if html else "-"
    display_employees.short_description = 'کارمندان مرتبط'

# No need for admin.site.register because @admin.register is used
