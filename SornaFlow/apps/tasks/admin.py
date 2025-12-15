from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Tasks
from apps.reports.admin import ReportsReadOnlyInline


@admin.register(Tasks) # راه بهتر برای ثبت ادمین
class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'truncated_description', 'display_employees',"is_active","created_at")
    search_fields = ('title', 'description', 'employees__name', 'employees__family',"is_active") # جستجو در نام کارمندان
    list_per_page = 15
    inlines = [ReportsReadOnlyInline]

    # 
    filter_horizontal = ('employees',)

    def truncated_description(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "بدون توضیحات"
    truncated_description.short_description = 'توضیحات مختصر'
    
    def display_employees(self, obj):
        """
        کارمندان مرتبط با این وظیفه را به صورت لیستی از لینک‌ها نمایش می‌دهد.
        """
        employees = obj.employees.all()
        if not employees:
            return "بدون کارمند"
        
        links = []
        for emp in employees:
            url = reverse('admin:accounts_employeeuser_change', args=[emp.pk])
        html = "<br>".join(links)
        return format_html(html) if html else "-"
            

    display_employees.short_description = 'کارمندان مرتبط'

# این خط دیگر لازم نیست چون از دکوراتور @admin.register استفاده کردیم
# admin.site.register(Tasks, TasksAdmin