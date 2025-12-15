from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels


class Tasks(models.Model):

    title = models.CharField(max_length=100, null=True, blank=True, verbose_name="عنوان وظیفه")
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات وظیفه')

    is_active=models.BooleanField(default=False,verbose_name="وضعیت فعال گزارش")

    start_date = jmodels.jDateTimeField(verbose_name="تاریخ شروع")
    end_date = jmodels.jDateTimeField(verbose_name="تاریخ پایان")

    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت گزارش")

    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True, # null=True حذف شد
        verbose_name="کارمندان مرتبط",
        related_name="tasks" # اضافه کردن related_name برای دسترسی بهتر
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "وظیفه"
        verbose_name_plural = "وظایف"