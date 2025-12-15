
# **README (English Version)**

# 🌟 **SornaFlow**

**SornaFlow** is an organizational web-based system built with **Django 6.0**, designed to streamline company operations, employee management, task assignment, and reporting workflows.  
It features a modular architecture, custom user model, Jalali date support, secure file uploads, and fully customized admin panels powered by environment-based configuration.

---

## 🚀 **Features**

- ✅ Custom user model (`EmployeeUser`) with complete personal & company fields  
- ✅ Company management with logo upload  
- ✅ Task assignment with automatic email notifications  
- ✅ Employee report submission with file attachments  
- ✅ Full Jalali date support (`django-jalali`)  
- ✅ Secure UUID‑based file upload paths  
- ✅ Environment variable–based configuration  
- ✅ Custom Django admin with image previews & read‑only inlines  
- ✅ Modular architecture with clean separation of concerns  
- ✅ Reusable HTML templates with shared CSS/JS assets  

---

## 📁 **Project Structure**

```
SornaFlow/
├── apps/
│   ├── accounts/                 # Authentication & employee management
│   ├── companies/                # Company information
│   ├── tasks/                    # Task management
│   ├── reports/                  # Report management
│   └── core/                     # Shared utilities (file upload handler)
(optional)
├── media/                        # Uploaded files
├── static/
│   ├── css/style.css
│   └── js/myscript.js
├── templates/
│   ├── main_template.html
│   ├── accounts_app/Login.html
│   └── tasks_app/employee_dashboard.html
├── .env.example                  # Environment variables template
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 📦 **Requirements**

```
asgiref==3.11.0
Django==6.0
django-jalali==7.4.0
django-jalali-date==2.0.0
jalali_core==1.0.0
jdatetime==5.2.0
mysqlclient==2.2.7
pillow==12.0.0
python-decouple==3.8
sqlparse==0.5.4
```

---

## ⚙️ **Installation & Setup**

### **1. Clone the repository**

```bash
git clone https://github.com/sorna-fast/SornaFlow.git
cd SornaFlow
```

### **2. Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your_strong_secret_key_here
DEBUG=True
DB_NAME=sorna_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@sornaflow.com
```

### **5. Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Create a superuser**

```bash
python manage.py createsuperuser
```

### **7. Run the server**

```bash
python manage.py runserver
```

---

## 🔐 **Authentication Flow**

- Employees log in via `/users/login/`  
- Admin users **cannot** log in through the employee login page  
- Successful login redirects to the employee dashboard  
- Logout available at `/users/logout/`  

---

## 🌐 **Important URLs**

| Feature | URL |
|--------|-----|
| Admin Panel | `/admin/` |
| Employee Login | `/users/login/` |
| Employee Logout | `/users/logout/` |
| Employee Dashboard | `/tasks/dashboard/` |

---

## 💡 **Project Improvements**

### ✅ Security
- Environment variables for sensitive data  
- UUID‑based secure file upload paths  

### ✅ Architecture
- Dedicated apps with clear separation of concerns  
- Shared utilities centralized in `apps/core/`  
- Optional service layer for business logic  

### ✅ User Experience
- Email notifications for task assignments  
- Responsive admin interface with image previews  
- Jalali date support for Persian calendar  

---

## 📬 **Contact**

- **GitHub:** [sorna-fast](https://github.com/sorna-fast)  
- **Email:** masudpythongit@gmail.com  
- **Telegram:** [@Masoud_Ghasemi_sorna_fast](https://t.me/Masoud_Ghasemi_sorna_fast)  
- **LinkedIn:** https://www.linkedin.com/in/masoud-ghasemi-748412381  

---

## 📝 **License**

This project is released under the terms of the included **[LICENSE](./LICENSE)** file.

---

# **نسخه فارسی README**

# 🌟 **SornaFlow**

**SornaFlow** یک سامانه سازمانی تحت وب مبتنی بر **Django 6.0** است که برای مدیریت شرکت‌ها، کارمندان، وظایف و گزارش‌ها طراحی شده است.  
این پروژه از معماری ماژولار، مدل کاربر سفارشی، تاریخ شمسی، آپلود امن فایل و پنل ادمین پیشرفته پشتیبانی می‌کند.

---

## 🚀 **ویژگی‌ها**

- ✅ مدل کاربر سفارشی با اطلاعات کامل پرسنلی  
- ✅ مدیریت شرکت‌ها همراه با آپلود لوگو  
- ✅ تخصیص وظایف با ارسال ایمیل  
- ✅ ثبت گزارش همراه با فایل ضمیمه  
- ✅ پشتیبانی از تاریخ شمسی (`django-jalali`)  
- ✅ مسیرهای آپلود امن مبتنی بر UUID  
- ✅ تنظیمات امن با متغیرهای محیطی  
- ✅ پنل ادمین سفارشی با پیش‌نمایش تصویر  
- ✅ معماری ماژولار با جداسازی مسئولیت‌ها  
- ✅ قالب‌های HTML ماژولار با CSS و JS مشترک  

---

## 📁 **ساختار پروژه**

```
SornaFlow/
├── apps/
│   ├── accounts/                 # مدیریت احراز هویت و کارمندان
│   ├── companies/                # اطلاعات شرکت‌ها
│   ├── tasks/                    # مدیریت وظایف
│   ├── reports/                  # مدیریت گزارشات
│   └── core/                     # ابزارهای مشترک (مدیریت آپلود فایل)
├── media/                        # فایل‌های آپلود شده
├── static/
│   ├── css/style.css
│   └── js/myscript.js
├── templates/
│   ├── main_template.html
│   ├── accounts/Login.html
│   └── tasks_app/employee_dashboard.html
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 📦 **وابستگی‌ها**

```
asgiref==3.11.0
Django==6.0
django-jalali==7.4.0
django-jalali-date==2.0.0
jalali_core==1.0.0
jdatetime==5.2.0
mysqlclient==2.2.7
pillow==12.0.0
python-decouple==3.8
sqlparse==0.5.4
```

---

## ⚙️ **نصب و راه‌اندازی**

### ۱. کلون کردن پروژه

```bash
git clone https://github.com/sorna-fast/SornaFlow.git
cd SornaFlow
```

### ۲. ساخت محیط مجازی

```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\activate
```

### ۳. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### ۴. تنظیم متغیرهای محیطی

```bash
cp .env.example .env
```

ویرایش `.env`:

```env
SECRET_KEY=your_strong_secret_key_here
DEBUG=True
DB_NAME=sorna_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@sornaflow.com
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

## 🔐 **احراز هویت**

- ورود کارمندان: `/users/login/`  
- عدم امکان ورود ادمین از این صفحه  
- هدایت به داشبورد پس از ورود موفق  
- خروج: `/users/logout/`  

---

## 🌐 **مسیرهای مهم**

| بخش | مسیر |
|-----|------|
| پنل ادمین | `/admin/` |
| ورود کارمند | `/users/login/` |
| خروج | `/users/logout/` |
| داشبورد کارمند | `/tasks/dashboard/` |

---

## 💡 **بهبودهای پروژه**

### ✅ امنیت
- استفاده از متغیرهای محیطی  
- مسیرهای آپلود امن مبتنی بر UUID  

### ✅ معماری
- اپ‌های اختصاصی با جداسازی مسئولیت‌ها  
- ابزارهای مشترک در `apps/core/`  
- لایه سرویس اختیاری  

### ✅ تجربه کاربری
- ارسال ایمیل هنگام تخصیص وظایف  
- پنل ادمین واکنش‌گرا با پیش‌نمایش فایل  
- پشتیبانی از تاریخ شمسی  

---

## 📬 **تماس**

- **گیت هاب:** [sorna-fast](https://github.com/sorna-fast)  
- **ایمیل:** masudpythongit@gmail.com  
- **تلگرام:** [@Masoud_Ghasemi_sorna_fast](https://t.me/Masoud_Ghasemi_sorna_fast)  
- **لینکدین:** https://www.linkedin.com/in/masoud-ghasemi-748412381  

---

## 📝 **مجوز**

این پروژه تحت مجوز موجود در فایل **[LICENSE](./LICENSE)** منتشر شده است.

---
