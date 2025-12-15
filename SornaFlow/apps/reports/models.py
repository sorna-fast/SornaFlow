from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels
from apps.core.utils import FileUpload
from apps.tasks.models import Tasks

# مدل گزارشات

file_upload = FileUpload('reports_files', 'reports_fields')
class Reports(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, verbose_name="وظیفه", related_name="reports")
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="کارمند ثبت کننده"
    )

    description = models.TextField(blank=True, null=True, verbose_name='توضیحات گزارش')
    STATUS_CHOICES = (
        ('2', 'درحال اجرا'), # ترتیب را برای نمایش بهتر تغییر دادیم
        ('1', 'موفق'),
        ('3', 'ناموفق'),
    )

    status = models.CharField(max_length=50, blank=True, choices=STATUS_CHOICES, default='2', null=True, verbose_name="وضعیت گزارش")

    file_upload_reports = models.FileField(upload_to=file_upload.upload_to, blank=True, null=True, verbose_name="فایل گزارش")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت گزارش")

    class Meta:
        verbose_name = "گزارش"
        verbose_name_plural = "گزارشات"
        ordering = ['-created_at'] # گزارش‌های جدیدتر بالاتر نمایش داده می‌شوند