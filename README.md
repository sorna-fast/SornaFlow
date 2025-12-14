# ✅ **README (English Version)**

# SornaFlow

**SornaFlow** is an organizational web-based system built with Django 6.0.  
It provides a complete workflow for managing companies, employees, tasks, and reports.  
The project uses a modular architecture, a custom user model, Jalali date support, file uploads, and fully customized admin panels.

---

## 🚀 Features

- Custom user model (`EmployeeUser`) with full personal and company-related fields  
- Company management with logo upload  
- Task assignment to employees  
- Employee report submission with file attachments  
- Jalali date support using `django-jalali`  
- UUID‑based file upload paths  
- Custom Django admin with image previews and read‑only inlines  
- Modular HTML templates with shared CSS/JS assets  

---

## 📁 Project Structure

```
SornaFlow/
├── apps/
│   ├── accounts/              # Authentication & employee management
│   ├── companies/             # Company information
│   └── tasks_and_reports/     # Tasks and employee reports
├── media/                     # Uploaded files
├── static/
│   ├── css/style.css
│   └── js/myscript.js
├── templates/
│   ├── main_template.html
│   ├── accounts_app/Login.html
│   └── tasks_and_reports/employee_panel.html
├── utils.py                   # FileUpload class
├── manage.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 📦 Requirements

```
asgiref==3.11.0
Django==6.0
django-jalali==7.4.0
django-jalali-date==2.0.0
jalali_core==1.0.0
jdatetime==5.2.0
mysqlclient==2.2.7
pillow==12.0.0
sqlparse==0.5.4
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd SornaFlow
```

### 2. Create a virtual environment

```bash
python -m venv myvenv
source myvenv/bin/activate      # Linux/macOS
myvenv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Edit `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sorna_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

---

## 🔐 Authentication Flow

- Employees log in via `/accounts/login/`
- Admin users **cannot** log in through the employee login page
- Successful login redirects to the employee dashboard
- Logout is available at `/accounts/logout/`

---

## 🌐 Important URLs

| Feature | URL |
|--------|-----|
| Admin Panel | `/admin/` |
| Employee Login | `/accounts/login/` |
| Employee Logout | `/accounts/logout/` |
| Employee Dashboard | `/tasks/employee_dashboard/` |

---
## Contact

- **GitHub**: [sorna-fast](https://github.com/sorna-fast)
- **Email**: [masudpythongit@gmail.com](mailto:masudpythongit@gmail.com)
- **Telegram**: [@Masoud_Ghasemi_sorna_fast](https://t.me/Masoud_Ghasemi_sorna_fast)

---

## 📝 License

This project is released under the terms of the included **[LICENSE](./LICENSE)** file.

---

# ✅ **نسخه فارسی README**

# SornaFlow

**SornaFlow** یک سامانه سازمانی تحت وب است که با Django 6.0 توسعه یافته و برای مدیریت شرکت‌ها، کارمندان، وظایف و گزارش‌ها طراحی شده است.  
این پروژه از مدل کاربر سفارشی، تاریخ شمسی، آپلود فایل، و پنل ادمین پیشرفته پشتیبانی می‌کند.

---

## 🚀 ویژگی‌ها

- مدل کاربر سفارشی با اطلاعات کامل پرسنلی  
- مدیریت شرکت‌ها همراه با آپلود لوگو  
- تخصیص وظایف به کارمندان  
- ثبت گزارش توسط کارمند همراه با فایل ضمیمه  
- پشتیبانی از تاریخ شمسی با `django-jalali`  
- مسیرهای آپلود مبتنی بر UUID  
- پنل ادمین سفارشی با پیش‌نمایش تصویر  
- قالب‌های HTML ماژولار با CSS و JS اختصاصی  

---

## 📁 ساختار پروژه

```
SornaFlow/
├── apps/
│   ├── accounts/              
│   ├── companies/             
│   └── tasks_and_reports/     
├── media/                     
├── static/
│   ├── css/style.css
│   └── js/myscript.js
├── templates/
│   ├── main_template.html
│   ├── accounts_app/Login.html
│   └── tasks_and_reports/employee_panel.html
├── utils.py
├── manage.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 📦 وابستگی‌ها

```
asgiref==3.11.0
Django==6.0
django-jalali==7.4.0
django-jalali-date==2.0.0
jalali_core==1.0.0
jdatetime==5.2.0
mysqlclient==2.2.7
pillow==12.0.0
sqlparse==0.5.4
```

---

## ⚙️ نصب و راه‌اندازی

### ۱. کلون کردن پروژه

```bash
git clone <your-repo-url>
cd SornaFlow
```

### ۲. ساخت محیط مجازی

```bash
python -m venv myvenv
source myvenv/bin/activate      # لینوکس/macOS
myvenv\Scripts\activate         # ویندوز
```

### ۳. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### ۴. تنظیم پایگاه داده

در فایل `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sorna_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### ۵. اعمال مایگریشن‌ها

```bash
python manage.py makemigrations
python manage.py migrate
```

### ۶. ساخت سوپر یوزر

```bash
python manage.py createsuperuser
```

### ۷. اجرای سرور

```bash
python manage.py runserver
```

---

## 🔐 احراز هویت

- ورود کارمندان از مسیر `/accounts/login/`  
- ادمین‌ها اجازه ورود از این صفحه را ندارند  
- پس از ورود موفق، کارمند به داشبورد هدایت می‌شود  
- خروج از سیستم در `/accounts/logout/`  

---

## 🌐 مسیرهای مهم

| بخش | مسیر |
|-----|------|
| پنل ادمین | `/admin/` |
| ورود کارمند | `/accounts/login/` |
| خروج | `/accounts/logout/` |
| داشبورد کارمند | `/tasks/employee_dashboard/` |

---
## تماس

- **گیت هاب**: [sorna-fast](https://github.com/sorna-fast)
- **ایمیل**: [masudpythongit@gmail.com](mailto:masudpythongit@gmail.com)
-   **تلگرام**: [@Masoud_Ghasemi_sorna_fast](https://t.me/Masoud_Ghasemi_sorna_fast)
---

## 📝 مجوز
 
این پروژه تحت مجوز موجود در فایل **[LICENSE](./LICENSE)** منتشر شده است.

---
