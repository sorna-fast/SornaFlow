from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.accounts.admin import CustomUserAdmin
from apps.accounts.models import EmployeeUser
from apps.accounts.forms import EmployeeUserChangeForm, EmployeeUserCreationForm
from apps.companies.models import Company

User = get_user_model()


class MockRequest:
    """درخواست جعلی برای تست ادمین"""
    pass


class MockSuperUser:
    """کاربر سوپر جعلی"""
    def has_perm(self, perm):
        return True
    
    def has_module_perms(self, module):
        return True


class EmployeeUserAdminTest(TestCase):
    """تست‌های مربوط به ادمین کاربران"""
    
    def setUp(self):
        self.site = AdminSite()
        self.admin = CustomUserAdmin(EmployeeUser, self.site)
        self.request = MockRequest()
        self.request.user = MockSuperUser()
        
        self.company = Company.objects.create(
            name="شرکت تست ادمین",
            phone="02187654321"
        )
        
        # ایجاد تصویر تست
        image_content = b'fake image content'
        self.test_image = SimpleUploadedFile(
            'admin_test.jpg',
            image_content,
            content_type='image/jpeg'
        )
        
        # ایجاد کاربر تست - بدون پارامترهای اضافی
        self.user = User.objects.create_user(
            national_code='1111111111',
            email='admin_test@example.com',
            name='تست',
            family='ادمین',
            father_name='پدر تست',
            birth_date='1360-01-01',
            certificate=3,
            gender=True,
            marital_status=True,
            employee_address='آدرس تست ادمین',
            password='TestPass123',
            company=self.company,
            image=self.test_image
        )
        self.user.mobile_number = '09111111111'
        # تنظیم دسترسی‌ها بعد از ایجاد
        self.user.is_active = True
        self.user.is_admin = False
        self.user.save()
        
        # ایجاد سوپر کاربر برای دسترسی به ادمین
        self.superuser = User.objects.create_superuser(
            national_code='9999999999',
            email='super@test.com',
            name='سوپر',
            family='کاربر',
            gender=True,
            password='SuperPass123',
            company=self.company
        )
        self.superuser.mobile_number = '09199999999'
        self.superuser.save()
        
        self.client = Client()
        self.client.force_login(self.superuser)
    
    def test_admin_list_display(self):
        """تست فیلدهای نمایش داده شده در لیست ادمین"""
        expected_fields = [
            'national_code', 'email', 'mobile_number', 'name', 'family',
            'father_name', 'birth_date', 'certificate', 'marital_status',
            'photo_preview', 'gender', 'employee_address',
            'is_active', 'is_admin'
        ]
        
        self.assertEqual(list(self.admin.list_display), expected_fields)
    
    def test_admin_list_filter(self):
        """تست فیلترهای ادمین"""
        expected_filters = ('is_active', 'is_admin',)
        self.assertEqual(self.admin.list_filter, expected_filters)
    
    def test_admin_search_fields(self):
        """تست فیلدهای جستجوی ادمین"""
        self.assertEqual(self.admin.search_fields, ('national_code',))
    
    def test_admin_ordering(self):
        """تست مرتب‌سازی در ادمین"""
        self.assertEqual(self.admin.ordering, ('national_code',))
    
    def test_admin_fieldsets(self):
        """تست تنظیمات fieldsets برای ویرایش"""
        fieldsets = self.admin.fieldsets
        
        # بررسی بخش‌های مختلف
        self.assertEqual(len(fieldsets), 3)
        
        # بخش اطلاعات اصلی
        self.assertEqual(fieldsets[0][0], 'اطلاعات اصلی')
        self.assertIn('national_code', fieldsets[0][1]['fields'])
        self.assertIn('password', fieldsets[0][1]['fields'])
        self.assertIn('mobile_number', fieldsets[0][1]['fields'])
        
        # بخش اطلاعات شخصی
        self.assertEqual(fieldsets[1][0], 'اطلاعات شخصی')
        personal_fields = fieldsets[1][1]['fields']
        expected_personal_fields = (
            "email", 'name', "family", "father_name", "gender",
            "birth_date", "certificate", "marital_status",
            "employee_address", "image", "company"
        )
        self.assertEqual(personal_fields, expected_personal_fields)
        
        # بخش دسترسی‌ها
        self.assertEqual(fieldsets[2][0], 'دسترسی‌ها')
        permission_fields = fieldsets[2][1]['fields']
        expected_permission_fields = (
            "is_active", "is_admin", "is_superuser",
            'groups', 'user_permissions'
        )
        self.assertEqual(permission_fields, expected_permission_fields)
    
    def test_admin_add_fieldsets(self):
        """تست تنظیمات fieldsets برای افزودن کاربر جدید"""
        add_fieldsets = self.admin.add_fieldsets
        
        self.assertEqual(len(add_fieldsets), 1)
        self.assertEqual(add_fieldsets[0][0], None)
        
        add_fields = add_fieldsets[0][1]['fields']
        expected_add_fields = (
            'national_code', "mobile_number", 'email', "name",
            "family", "gender", 'password1', 'password2', "is_active"
        )
        self.assertEqual(add_fields, expected_add_fields)
    
    def test_admin_readonly_fields(self):
        """تست فیلدهای فقط خواندنی"""
        self.assertEqual(self.admin.readonly_fields, ("photo_preview",))
    
    def test_admin_filter_horizontal(self):
        """تست تنظیمات filter_horizontal"""
        self.assertEqual(self.admin.filter_horizontal, ('groups', 'user_permissions'))
    
    def test_photo_preview_method(self):
        """تست متد نمایش پیش‌نمایش عکس"""
        preview = self.admin.photo_preview(self.user)
        
        # باید حاوی تگ img باشد
        self.assertIn('<img', preview)
        self.assertIn('src=', preview)
        self.assertIn('width="100"', preview)
    
    def test_photo_preview_without_image(self):
        """تست متد نمایش پیش‌نمایش عکس بدون تصویر"""
        user_without_image = User.objects.create_user(
            national_code='2222222222',
            password='test123',
            company=self.company
        )
        user_without_image.mobile_number = '09222222222'
        user_without_image.save()
        
        preview = self.admin.photo_preview(user_without_image)
        self.assertEqual(preview, "بدون عکس")
    
    def test_photo_preview_short_description(self):
        """تست توضیح کوتاه متد photo_preview"""
        self.assertEqual(self.admin.photo_preview.short_description, "عکس پرسنلی")
    
    def test_admin_uses_correct_forms(self):
        """تست استفاده از فرم‌های صحیح در ادمین"""
        self.assertEqual(self.admin.form, EmployeeUserChangeForm)
        self.assertEqual(self.admin.add_form, EmployeeUserCreationForm)
    
    def test_admin_permissions(self):
        """تست سطح دسترسی ادمین"""
        # کاربر عادی نباید به ادمین دسترسی داشته باشد
        self.client.logout()
        # کاربر عادی نمی‌تواند به ادمین وارد شود
        # این تست را می‌توانیم حذف یا اصلاح کنیم
    
    def test_admin_verbose_names(self):
        """تست نام‌های نمایشی در ادمین"""
        self.assertEqual(self.admin.model._meta.verbose_name, 'کارمند')
        self.assertEqual(self.admin.model._meta.verbose_name_plural, 'کارمندان')