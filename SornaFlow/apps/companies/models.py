from django.db import models
from utils import FileUpload
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100,verbose_name="اسم شرکت")
    address_company = models.CharField(max_length=200,verbose_name="ادرس شرکت")
    phone = models.CharField(max_length=20,null=True,blank=True,verbose_name="شماره تماس شرکت")
    file_upload =FileUpload("images","image_logo")
    logo=models.ImageField(upload_to=file_upload.upload_to,blank=True,null=True,verbose_name="عکس لگو شرکت")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="شرکت"
        verbose_name_plural="شرکت ها"
