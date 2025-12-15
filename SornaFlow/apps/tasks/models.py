from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels


class Tasks(models.Model):

    title = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="عنوان وظیفه"
    )  # Optional task title

    description = models.TextField(
        blank=True, null=True,
        verbose_name='توضیحات وظیفه'
    )  # Optional detailed description

    is_active = models.BooleanField(
        default=False,
        verbose_name="وضعیت فعال گزارش"
    )  # Controls task activation status

    start_date = jmodels.jDateTimeField(
        verbose_name="تاریخ شروع"
    )  # Jalali start datetime

    end_date = jmodels.jDateTimeField(
        verbose_name="تاریخ پایان"
    )  # Jalali end datetime

    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت گزارش"
    )  # Timestamp when task is created

    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="کارمندان مرتبط",
        related_name="tasks"
    )  # Employees assigned to this task

    def __str__(self):
        return self.title  # Display task title in admin

    class Meta:
        verbose_name = "وظیفه"          # Singular name in admin
        verbose_name_plural = "وظایف"   # Plural name in admin
