from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels
from apps.core.utils import FileUpload
from apps.tasks.models import Tasks

# File upload handler for report attachments
file_upload = FileUpload('reports_files', 'reports_fields')


class Reports(models.Model):
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        verbose_name="وظیفه",
        related_name="reports"
    )  # Link each report to a specific task

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="کارمند ثبت کننده"
    )  # Employee who submitted the report

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات گزارش'
    )  # Optional report description

    STATUS_CHOICES = (
        ('2', 'درحال اجرا'),  # In progress
        ('1', 'موفق'),        # Successful
        ('3', 'ناموفق'),      # Failed
    )

    status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=STATUS_CHOICES,
        default='2',
        verbose_name="وضعیت گزارش"
    )  # Report status field

    file_upload_reports = models.FileField(
        upload_to=file_upload.upload_to,
        blank=True,
        null=True,
        verbose_name="فایل گزارش"
    )  # Optional file attachment

    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت گزارش"
    )  # Timestamp when report is created

    class Meta:
        verbose_name = "گزارش"              # Singular name in admin
        verbose_name_plural = "گزارشات"     # Plural name in admin
        ordering = ['-created_at']          # Newest reports first
