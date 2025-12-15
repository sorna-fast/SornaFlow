from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import EmployeeUser
#________________________________________________________________________________________________________________________________________________


class EmployeeUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)  # First password input
    password2 = forms.CharField(label="RePassword", widget=forms.PasswordInput)  # Password confirmation field

    class Meta:
        model = EmployeeUser  # Model associated with this form
        fields = [
            'national_code', "mobile_number", 'email', "name",
            "family", "image", "gender", "company"
        ]  # Fields included in the creation form

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]  # First password value
        pass2 = self.cleaned_data["password2"]  # Second password value
        if pass1 and pass2 and pass1 != pass2:  # Validate password match
            raise ValidationError("رمز عبور و تکرار ان با عم مغایرت دارند")
        return pass2  # Return confirmed password

    def save(self, commit=True):
        user = super().save(commit=False)  # Create user instance without saving
        user.set_password(self.cleaned_data['password1'])  # Hash and set password
        if commit:
            user.save()  # Save user to database
        return user  # Return created user instance


#________________________________________________________________________________________________________________________________________________


class EmployeeUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="برای تغییر رمز عبور روی این <a href='../password'>لینک</a> کلیک کنید"
    )  # Read‑only hashed password field

    class Meta:
        model = EmployeeUser  # Model associated with this form
        fields = [
            'national_code', "mobile_number", 'email', "name",
            "family", "image", "gender", "is_active", "is_admin", "company"
        ]  # Fields allowed to be edited


#________________________________________________________________________________________________________________________________________________


class LoginUserForm(forms.Form):
    national_code = forms.CharField(
        label="کد ملی",
        error_messages={"required": "این فیلد نمیتواند خالی باد"},  # Custom required error
        widget=forms.TextInput(attrs={
            'class': "form-control",
            "placeholder": " کد ملی را وارد کنید"
        })  # Styled text input
    )

    password = forms.CharField(
        label="رمز ورود",
        error_messages={"required": "این فیلد نمیتواند خالی باد"},  # Custom required error
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            "placeholder": " رمز را وارد کنید"
        })  # Styled password input
    )
