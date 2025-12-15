from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django_jalali.db import models as jmodels
from apps.core.utils import FileUpload
#___________________________________________________________________________________

class EmployeesUserManager(BaseUserManager):
    def create_user(self,national_code,email="",name="",family="",father_name="",birth_date=None,certificate=None,gender=None,marital_status=None,employee_address=None,password=None,company=None,image=None):
        if not national_code:
            raise ValueError("کد ملی باید وارد شود")
        
        user=self.model(
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
        user.set_password(password)
        user.save(using=self._db)
        return user
    #----------------------------------
    def create_superuser(self,national_code,email,name,family,password=None,gender=None,company=None,image=None):
        user=self.create_user(national_code=national_code,
                         email=email,
                         name=name,
                         family=family,
                         gender=gender,
                         password=password,
                         company=company,
                         image=image)
        
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
#___________________________________________________________________________________
from apps.companies.models import Company

from django.conf import settings

class EmployeeUser(AbstractBaseUser,PermissionsMixin):
    national_code=models.CharField(max_length=11,unique=True,verbose_name="کد ملی")
    email=models.EmailField(max_length=200,blank=True,verbose_name="ایمیل")
    mobile_number=models.CharField(max_length=11,unique=True,verbose_name="شماره موبایل")
    name=models.CharField(max_length=50,blank=True,verbose_name="نام")
    family=models.CharField(max_length=50,blank=True,verbose_name="نام خانوادگی")
    father_name=models.CharField(max_length=50,blank=True,verbose_name="نام پدر")
    birth_date = jmodels.jDateField(null=True, blank=True,verbose_name="تاریخ تولد")
    CERTIFICATE_CHOICES=((1,'دیپلم'),(2,"کارشناسی"),(3,"کارشناسی ارشد"),(4,"دکتری"),)
    certificate=models.IntegerField(blank=True,null=True,verbose_name="مدرک تحصیلی",choices=CERTIFICATE_CHOICES)
    MARITALSTATUS_CHOICES=((True,'بله'),(False,"خیر"),)
    marital_status=models.BooleanField(max_length=50,blank=True,choices=MARITALSTATUS_CHOICES,default='True',null=True,verbose_name="وظعیت تاهل")
    GENDER_CHOICES=((True,'مرد'),(False,"زن"),)
    gender=models.BooleanField(max_length=50,blank=True,choices=GENDER_CHOICES,default='True',null=True,verbose_name="جنسیت")
    register_date=jmodels.jDateTimeField(auto_now_add=True)
    employee_address = models.TextField(blank=True, null=True, verbose_name='ادرس محل سکونت کارمند')
    is_active=models.BooleanField(default=False,verbose_name="وضعیت فعال")
    is_admin=models.BooleanField(default=False,verbose_name="وضعیت هماهنگ کننده")
    USERNAME_FIELD='national_code'
    REQUIRED_FIELDS=["email",'name','family']
    
    objects = EmployeesUserManager()
    
    company = models.ForeignKey(  # فیلد جدید
        Company,
        on_delete=models.SET_NULL,  # اگر شرکت حذف شد، کارمند حذف نشود
        null=True,
        blank=True,
        verbose_name="شرکت"
    )

    file_upload=FileUpload("images","personal_photo")
    image=models.ImageField(upload_to=file_upload.upload_to,blank=True,null=True,verbose_name="اپلود عکس")

    def __str__(self):
        return self.name+" "+self.family

    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name="کارمند"
        verbose_name_plural="کارمندان"
#___________________________________________________________________________________

