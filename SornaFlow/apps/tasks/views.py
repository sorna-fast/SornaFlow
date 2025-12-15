from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tasks
from apps.reports.models import Reports
from django.contrib import messages  
from django.db.models import Q
from django_jalali.db import models as jmodels
@login_required
def employee_dashboard(request):
    current_employee = request.user

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        description = request.POST.get('description')
        status = request.POST.get('status')  # مقدار از فیلد مخفی خوانده می‌شود
        uploaded_file = request.FILES.get('file')

        # ۲. اعتبارسنجی سمت سرور: مطمئن می‌شویم که وضعیت خالی نیست
        if task_id and status and status in ["درحال اجرا", "موفق", "ناموفق"]:
            task_instance = get_object_or_404(Tasks, id=task_id)
            
            Reports.objects.create(
                task=task_instance,
                employee=current_employee,
                description=description,
                status=status,
                file_upload_reports=uploaded_file
            )
            # ۳. پیام موفقیت برای کاربر
            messages.success(request, 'گزارش شما با موفقیت ثبت شد.')
        else:
            # ۴. پیام خطا در صورت عدم انتخاب وضعیت
            messages.error(request, 'خطا: لطفاً وضعیت وظیفه را انتخاب کنید.')
        
        return redirect('tasks_app:employee_dashboard')

    assigned_tasks = Tasks.objects.filter(
        Q(employees=current_employee) &
        Q(is_active=True) &
        Q(start_date__lte=jmodels.timezone.now()) &
        Q(end_date__gte=jmodels.timezone.now())).prefetch_related('reports').order_by('title')

    context = {
        'tasks': assigned_tasks,
    }
    return render(request, 'tasks_app/employee_panel.html', context)