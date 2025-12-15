from django.urls import path
from . import views

app_name = "tasks_app"  # Namespace for URL reversing

urlpatterns = [
    path('', views.employee_dashboard, name='employee_dashboard'),  # Employee dashboard route
]
