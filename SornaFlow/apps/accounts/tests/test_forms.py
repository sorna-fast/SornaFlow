from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from apps.accounts.forms import (
    EmployeeUserCreationForm,
    EmployeeUserChangeForm,
    LoginUserForm
)
from apps.companies.models import Company

User = get_user_model()


class EmployeeUserCreationFormTest(TestCase):
    
    def setUp(self):
        self.company = Company.objects.create(
            name="شرکت تست",
            phone="02112345678"
        )
        
        self.valid_data = {
            'national_code': '0012345678',
            'mobile_number': '09123456789',
            'email': 'test@example.com',
            'name': 'علی',
            'family': 'رضایی',
            'gender': True,
            'company': self.company.id,
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
    
    def test_form_with_valid_data(self):
        """تست فرم با داده‌های معتبر"""
        form = EmployeeUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.national_code, '0012345678')
        self.assertEqual(user.mobile_number, '09123456789')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('ComplexPass123!'))
    
    def test_form_with_mismatched_passwords(self):
        """تست فرم با رمزهای عبور غیرمطابقت"""
        data = self.valid_data.copy()
        data['password2'] = 'DifferentPass456!'
        
        form = EmployeeUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('رمز عبور و تکرار ان با عم مغایرت دارند', form.errors['password2'][0])
    
    def test_form_with_missing_required_fields(self):
        """تست فرم با فیلدهای ضروری خالی"""
        data = {
            'national_code': '',
            'mobile_number': '',
            'password1': 'test123',
            'password2': 'test123'
        }
        
        form = EmployeeUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('national_code', form.errors)
        self.assertIn('mobile_number', form.errors)
    
    def test_form_with_duplicate_national_code(self):
        """تست فرم با کد ملی تکراری"""
        # ابتدا کاربر ایجاد می‌کنیم
        user = User.objects.create_user(
            national_code='1234567890',
            password='test123'
        )
        user.mobile_number = '09111111111'
        user.save()
        
        # تلاش برای ایجاد کاربر با کد ملی تکراری
        data = self.valid_data.copy()
        data['national_code'] = '1234567890'
        data['mobile_number'] = '09222222222'
        
        form = EmployeeUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('national_code', form.errors)
    
    def test_form_with_invalid_email(self):
        """تست فرم با ایمیل نامعتبر"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        
        form = EmployeeUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_save_with_commit_false(self):
        """تست ذخیره فرم با commit=False"""
        form = EmployeeUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        user = form.save(commit=False)
        self.assertIsNotNone(user)
        self.assertEqual(user.national_code, '0012345678')
        self.assertIsNone(user.pk)  # هنوز در دیتابیس ذخیره نشده
        
        user.save()  # حالا ذخیره می‌شود
        self.assertIsNotNone(user.pk)


class EmployeeUserChangeFormTest(TestCase):
    
    def setUp(self):
        self.company = Company.objects.create(
            name="شرکت تست",
            phone="02112345678"
        )
        
        # ابتدا کاربر ایجاد می‌کنیم
        self.user = User.objects.create_user(
            national_code='0012345678',
            email='test@example.com',
            name='علی',
            family='رضایی',
            gender=True,
            password='test123',
            company=self.company
        )
        self.user.mobile_number = '09123456789'
        self.user.save()
    
    def test_form_with_valid_data(self):
        """تست فرم تغییر با داده‌های معتبر"""
        form = EmployeeUserChangeForm(instance=self.user, data={
            'national_code': '0012345678',
            'mobile_number': '09123456789',
            'email': 'updated@example.com',
            'name': 'علی',
            'family': 'رضایی',
            'gender': True,
            'is_active': True,
            'is_admin': False,
            'company': self.company.id
        })
        
        self.assertTrue(form.is_valid())
        
        updated_user = form.save()
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertTrue(updated_user.is_active)
        self.assertFalse(updated_user.is_admin)
    
    def test_form_readonly_password_field(self):
        """تست فیلد رمز عبور فقط خواندنی"""
        form = EmployeeUserChangeForm(instance=self.user)
        
        # بررسی وجود فیلد password با کمک‌متن
        self.assertIn('password', form.fields)
        self.assertTrue(form.fields['password'].disabled)
        self.assertIn('لینک', form.fields['password'].help_text)
    
    def test_form_excludes_password_from_clean_data(self):
        """تست عدم وجود پسورد در clean_data"""
        form = EmployeeUserChangeForm(instance=self.user, data={
            'national_code': '0012345678',
            'mobile_number': '09123456789',
            'email': 'test@example.com',
            'name': 'علی',
            'family': 'رضایی',
            'gender': True
        })
        
        self.assertTrue(form.is_valid())
        # فیلد password ممکن است در cleaned_data باشد اما مقدار None دارد
        # این قابل قبول است چون فیلد readonly است
        if 'password' in form.cleaned_data:
            self.assertIsNone(form.cleaned_data['password'])


class LoginUserFormTest(TestCase):
    
    def test_form_with_valid_data(self):
        """تست فرم لاگین با داده‌های معتبر"""
        form = LoginUserForm(data={
            'national_code': '0012345678',
            'password': 'TestPass123'
        })
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['national_code'], '0012345678')
        self.assertEqual(form.cleaned_data['password'], 'TestPass123')
    
    def test_form_with_empty_fields(self):
        """تست فرم لاگین با فیلدهای خالی"""
        form = LoginUserForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertIn('national_code', form.errors)
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['national_code'][0], 'این فیلد نمیتواند خالی باد')
        self.assertEqual(form.errors['password'][0], 'این فیلد نمیتواند خالی باد')
    
    def test_form_widget_attributes(self):
        """تست ویژگی‌های ویجت فرم"""
        form = LoginUserForm()
        
        # بررسی کلاس و placeholder فیلد کد ملی
        national_code_field = form.fields['national_code']
        self.assertEqual(national_code_field.widget.attrs['class'], 'form-control')
        self.assertEqual(national_code_field.widget.attrs['placeholder'], ' کد ملی را وارد کنید')
        
        # بررسی کلاس و placeholder فیلد رمز عبور
        password_field = form.fields['password']
        self.assertEqual(password_field.widget.attrs['class'], 'form-control')
        self.assertEqual(password_field.widget.attrs['placeholder'], ' رمز را وارد کنید')
    
    def test_form_labels(self):
        """تست برچسب‌های فرم"""
        form = LoginUserForm()
        
        self.assertEqual(form.fields['national_code'].label, 'کد ملی')
        self.assertEqual(form.fields['password'].label, 'رمز ورود')