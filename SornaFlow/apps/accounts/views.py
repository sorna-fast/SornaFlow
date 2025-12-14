from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import LoginUserForm
from .models import EmployeeUser
from django.views import View
from django.conf import settings

def media_admin(request):
    return {"media_url":settings.MEDIA_URL}


class LoginUserView(View):
    template_name="accounts_app/Login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("tasks_and_reports_app:employee_dashboard")
        return super().dispatch(request, *args, **kwargs)

    
    def get(self,request,*args, **kwargs):
        form=LoginUserForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request,*args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data['national_code'],password=data['password'])
            if user is not None:
                db_user=EmployeeUser.objects.get(national_code=data['national_code'])

                if db_user.is_admin==False:
                    messages.success(request,"ورود با موفقیت انجام شد",'success')
                    login(request,user)
                    next_url=request.GET.get('next')
                    if next_url is not None:
                        return redirect((next_url))
                    else:
                        return redirect("tasks_and_reports_app:employee_dashboard")
                else:
                    messages.error(request,"کاربر ادمین نمیتواند از اینجا وارد شود",'warning')
                    return render(request,self.template_name,{'form':form})
            else:
                messages.error(request,"اطلاعات کاربری وارد شده نادرست است","danger")
                return render(request,self.template_name,{'form':form})
        else:
            messages.error(request,"اطلاعات وارد شده نامعتبر است","danger")
            return render(request,self.template_name,{'form':form})


class LogoutView(View):
    def get(self, request):
        # لاگ‌اوت کاربر و پاکسازی سشن
        logout(request)
        messages.success(request, "شما با موفقیت از سیستم خارج شدید.")
        return redirect('accounts_app:login')  # تغییر به نام URL صفحه لاگین شما
    
    # برای امنیت بیشتر می‌توانید از POST استفاده کنید
    def post(self, request):
        return self.get(request)