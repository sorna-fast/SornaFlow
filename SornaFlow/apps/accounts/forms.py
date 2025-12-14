from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import EmployeeUser
#________________________________________________________________________________________________________________________________________________



class EmployeeUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="RePassword",widget=forms.PasswordInput)
    class Meta:
        model=EmployeeUser
        fields=['national_code',"mobile_number",'email',"name","family","image","gender","company"]

    def clean_password2(self):
        pass1= self.cleaned_data["password1"]
        pass2= self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار ان با عم مغایرت دارند")
        return pass2
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


#________________________________________________________________________________________________________________________________________________


class EmployeeUserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور روی این <a href='../password'>لینک</a> کلیک کنید")
    class Meta:
        model=EmployeeUser
        fields=['national_code',"mobile_number",'email',"name","family","image","gender","is_active","is_admin","company"]








#________________________________________________________________________________________________________________________________________________
class LoginUserForm(forms.Form):
    national_code=forms.CharField(label="کد ملی",
                                  error_messages={"required":"این فیلد نمیتواند خالی باد"},
                                  widget=forms.TextInput(attrs={'class':"form-control","placeholder":" کد ملی را وارد کنید"}))
    password=forms.CharField(label="رمز ورود",
                                  error_messages={"required":"این فیلد نمیتواند خالی باد"},
                                  widget=forms.PasswordInput(attrs={'class':"form-control","placeholder":" رمز را وارد کنید"}))