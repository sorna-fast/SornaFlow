from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_jalali.db import models as jmodels
from apps.core.utils import FileUpload
#___________________________________________________________________________________


class EmployeesUserManager(BaseUserManager):
    def create_user(
        self, national_code, email="", name="", family="", father_name="",
        birth_date=None, certificate=None, gender=None, marital_status=None,
        employee_address=None, password=None, company=None, image=None
    ):
        if not national_code:  # Ensure national code is provided
            raise ValueError("کد ملی باید وارد شود")

        # Create user instance with provided fields
        user = self.model(
            national_code=national_code,
            email=self.normalize_email(email),
            name=name,
            family=family,
            father_name=father_name,
            birth_date=birth_date,
            certificate=certificate,
            gender=gender,
            marital_status=marital_status,
            employee_address=employee_address,
            company=company,
            image=image
        )
        user.set_password(password)  # Hash and set password
        user.save(using=self._db)  # Save user to database
        return user

    #----------------------------------
    def create_superuser(self, national_code, email, name, family,
                         password=None, gender=None, company=None, image=None):
        # Create a regular user first
        user = self.create_user(
            national_code=national_code,
            email=email,
            name=name,
            family=family,
            gender=gender,
            password=password,
            company=company,
            image=image
        )

        # Grant admin and superuser privileges
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
#___________________________________________________________________________________

from apps.companies.models import Company
from django.conf import settings


class EmployeeUser(AbstractBaseUser, PermissionsMixin):
    national_code = models.CharField(
        max_length=11, unique=True, verbose_name="کد ملی"
    )  # Unique identifier used for login
    email = models.EmailField(
        max_length=200, blank=True, verbose_name="ایمیل"
    )  # Optional email field
    mobile_number = models.CharField(
        max_length=11, unique=True, verbose_name="شماره موبایل"
    )  # Unique mobile number
    name = models.CharField(
        max_length=50, blank=True, verbose_name="نام"
    )  # First name
    family = models.CharField(
        max_length=50, blank=True, verbose_name="نام خانوادگی"
    )  # Last name
    father_name = models.CharField(
        max_length=50, blank=True, verbose_name="نام پدر"
    )  # Father's name
    birth_date = jmodels.jDateField(
        null=True, blank=True, verbose_name="تاریخ تولد"
    )  # Jalali birth date

    CERTIFICATE_CHOICES = (
        (1, 'دیپلم'),
        (2, "کارشناسی"),
        (3, "کارشناسی ارشد"),
        (4, "دکتری"),
    )
    certificate = models.IntegerField(
        blank=True, null=True, choices=CERTIFICATE_CHOICES, verbose_name="مدرک تحصیلی"
    )  # Education level

    MARITALSTATUS_CHOICES = ((True, 'بله'), (False, "خیر"))
    marital_status = models.BooleanField(
        max_length=50, blank=True, null=True,
        choices=MARITALSTATUS_CHOICES, default='True',
        verbose_name="وظعیت تاهل"
    )  # Marital status

    GENDER_CHOICES = ((True, 'مرد'), (False, "زن"))
    gender = models.BooleanField(
        max_length=50, blank=True, null=True,
        choices=GENDER_CHOICES, default='True',
        verbose_name="جنسیت"
    )  # Gender

    register_date = jmodels.jDateTimeField(
        auto_now_add=True
    )  # Auto timestamp on creation

    employee_address = models.TextField(
        blank=True, null=True, verbose_name='ادرس محل سکونت کارمند'
    )  # Optional address field

    is_active = models.BooleanField(
        default=False, verbose_name="وضعیت فعال"
    )  # Controls login permission
    is_admin = models.BooleanField(
        default=False, verbose_name="وضعیت هماهنگ کننده"
    )  # Admin/staff flag

    USERNAME_FIELD = 'national_code'  # Field used for authentication
    REQUIRED_FIELDS = ["email", 'name', 'family']  # Required when creating superuser

    objects = EmployeesUserManager()  # Custom manager

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,  # Keep employee if company is deleted
        null=True,
        blank=True,
        verbose_name="شرکت"
    )  # Company relation

    file_upload = FileUpload("images", "personal_photo")  # Upload path generator
    image = models.ImageField(
        upload_to=file_upload.upload_to, blank=True, null=True, verbose_name="اپلود عکس"
    )  # Profile image

    def __str__(self):
        return self.name + " " + self.family  # Display full name

    @property
    def is_staff(self):
        return self.is_admin  # Required by Django admin

    class Meta:
        verbose_name = "کارمند"
        verbose_name_plural = "کارمندان"  # Admin display names
#___________________________________________________________________________________
