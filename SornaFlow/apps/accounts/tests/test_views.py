from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import AnonymousUser
from unittest.mock import patch, Mock
from django.http import HttpResponseRedirect
from apps.accounts.views import LoginUserView, LogoutView, media_admin
from apps.accounts.forms import LoginUserForm
from apps.companies.models import Company

User = get_user_model()


class LoginUserViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.company = Company.objects.create(
            name="شرکت تست",
            phone="02112345678"
        )
        
        # ایجاد کاربر عادی (غیر ادمین)
        self.regular_user = User.objects.create_user(
            national_code='0012345678',
            name='کاربر',
            family='عادی',
            password='TestPass123',
            company=self.company
        )
        self.regular_user.mobile_number = '09123456789'
        self.regular_user.is_active = True
        self.regular_user.save()
        
        # ایجاد کاربر ادمین
        self.admin_user = User.objects.create_superuser(
            national_code='0098765432',
            email='admin@test.com',
            name='مدیر',
            family='سیستم',
            gender=True,
            password='AdminPass123',
            company=self.company
        )
        self.admin_user.mobile_number = '09123456788'
        self.admin_user.is_active = True
        self.admin_user.save()
        
        self.login_url = reverse('accounts_app:login')
    
    def test_login_view_get_request(self):
        """تست درخواست GET به صفحه لاگین"""
        response = self.client.get(self.login_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/Login.html')
        self.assertIsInstance(response.context['form'], LoginUserForm)
    
    @patch('apps.accounts.views.redirect')
    def test_login_view_redirects_authenticated_user(self, mock_redirect):
        """تست ریدایرکت کاربر احراز هویت شده"""
        # Mock کردن redirect
        mock_redirect.return_value = HttpResponseRedirect('/dashboard/')
        
        self.client.login(national_code='0012345678', password='TestPass123')
        response = self.client.get(self.login_url, follow=False)
        
        # باید ریدایرکت شود
        self.assertEqual(response.status_code, 302)
    
    @patch('apps.accounts.views.redirect')
    def test_successful_login_regular_user(self, mock_redirect):
        """تست لاگین موفق کاربر عادی"""
        # Mock کردن redirect
        mock_redirect.return_value = HttpResponseRedirect('/dashboard/')
        
        response = self.client.post(self.login_url, {
            'national_code': '0012345678',
            'password': 'TestPass123'
        }, follow=False)
        
        # باید لاگین شده باشد
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # بررسی پیام موفقیت
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'ورود با موفقیت انجام شد')
        self.assertIn('success', messages[0].tags)
    
    def test_unsuccessful_login_wrong_credentials(self):
        """تست لاگین با اطلاعات نادرست"""
        response = self.client.post(self.login_url, {
            'national_code': '0012345678',
            'password': 'WrongPassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/Login.html')
        
        # بررسی پیام خطا
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'اطلاعات کاربری وارد شده نادرست است')
        self.assertIn('danger', messages[0].tags)
    
    def test_admin_user_cannot_login_from_this_view(self):
        """تست عدم امکان لاگین کاربر ادمین از این ویو"""
        response = self.client.post(self.login_url, {
            'national_code': '0098765432',
            'password': 'AdminPass123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/Login.html')
        
        # بررسی پیام خطا
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'کاربر ادمین نمیتواند از اینجا وارد شود')
        self.assertIn('warning', messages[0].tags)
    
    def test_login_with_inactive_user(self):
        """تست لاگین کاربر غیرفعال"""
        inactive_user = User.objects.create_user(
            national_code='0000000000',
            password='TestPass123',
            company=self.company
        )
        inactive_user.mobile_number = '09000000000'
        inactive_user.is_active = False
        inactive_user.save()
        
        response = self.client.post(self.login_url, {
            'national_code': '0000000000',
            'password': 'TestPass123'
        })
        
        self.assertEqual(response.status_code, 200)
        
        # کاربر غیرفعال نمی‌تواند وارد شود
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('اطلاعات کاربری وارد شده نادرست است', messages[0].message)
    
    def test_login_with_invalid_form_data(self):
        """تست لاگین با داده‌های فرم نامعتبر"""
        response = self.client.post(self.login_url, {
            'national_code': '',  # فیلد خالی
            'password': ''
        })
        
        self.assertEqual(response.status_code, 200)
        
        # بررسی پیام خطای فرم
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'اطلاعات وارد شده نامعتبر است')
        self.assertIn('danger', messages[0].tags)
    
    @patch('apps.accounts.views.redirect')
    def test_login_redirects_to_next_url(self, mock_redirect):
        """تست ریدایرکت به URL بعدی بعد از لاگین"""
        next_url = '/some/other/page/'
        
        # Mock کردن redirect
        mock_redirect.return_value = HttpResponseRedirect(next_url)
        
        response = self.client.post(
            f'{self.login_url}?next={next_url}',
            {
                'national_code': '0012345678',
                'password': 'TestPass123'
            },
            follow=False
        )
        
        # باید ریدایرکت شود
        self.assertEqual(response.status_code, 302)
    
    def test_login_view_context(self):
        """تست context برگردانده شده توسط ویو"""
        response = self.client.get(self.login_url)
        
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], LoginUserForm)
    
    def test_view_methods(self):
        """تست متدهای view"""
        view = LoginUserView()
        
        # بررسی ویژگی‌های view
        self.assertEqual(view.template_name, 'accounts_app/Login.html')
        
        # تست dispatch با کاربر احراز هویت شده (با patch)
        with patch('apps.accounts.views.redirect') as mock_redirect:
            mock_redirect.return_value = HttpResponseRedirect('/dashboard/')
            
            request = self.factory.get(self.login_url)
            request.user = self.regular_user
            request.session = {}
            request._messages = Mock()
            
            response = view.dispatch(request)
            self.assertEqual(response.status_code, 302)
            mock_redirect.assert_called_once_with("tasks_app:employee_dashboard")
    
    def test_class_based_view_attributes(self):
        """تست ویژگی‌های کلاس‌بیس ویو"""
        view = LoginUserView()
        self.assertEqual(view.template_name, 'accounts_app/Login.html')