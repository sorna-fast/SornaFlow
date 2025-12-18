from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginUserForm
from .models import EmployeeUser
from django.views import View
from django.conf import settings


def media_admin(request):
    return {"media_url": settings.MEDIA_URL}  # Exposes MEDIA_URL to templates


class LoginUserView(View):
    template_name = "accounts_app/Login.html"  # Template for login page

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users away from login page
        if request.user.is_authenticated:
            return redirect("tasks_app:employee_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = LoginUserForm()  # Empty login form
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)  # Bind form with POST data
        if form.is_valid():
            data = form.cleaned_data  # Extract validated fields
            user = authenticate(
                username=data['national_code'],
                password=data['password']
            )  # Authenticate user

            if user is not None:
                db_user = EmployeeUser.objects.get(
                    national_code=data['national_code']
                )  # Fetch user record

                if db_user.is_admin is False:  # Prevent admin login here
                    messages.success(request, "ورود با موفقیت انجام شد", 'success')
                    login(request, user)  # Log user in

                    next_url = request.GET.get('next')  # Handle redirect after login
                    if next_url is not None:
                        return redirect(next_url)
                    return redirect("tasks_app:employee_dashboard")

                else:
                    messages.error(
                        request,
                        "کاربر ادمین نمیتواند از اینجا وارد شود",
                        'warning'
                    )  # Admin login blocked
                    return render(request, self.template_name, {'form': form})

            else:
                messages.error(
                    request,
                    "اطلاعات کاربری وارد شده نادرست است",
                    "danger"
                )  # Invalid credentials
                return render(request, self.template_name, {'form': form})

        else:
            messages.error(
                request,
                "اطلاعات وارد شده نامعتبر است",
                "danger"
            )  # Form validation failed
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)  # Clear session and log user out
        messages.success(request, "شما با موفقیت از سیستم خارج شدید.")
        return redirect('accounts_app:login')  # Redirect to login page

    def post(self, request):
        return self.get(request)  # POST fallback for logout
