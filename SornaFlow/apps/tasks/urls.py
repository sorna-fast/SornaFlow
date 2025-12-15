from django.urls import path
from . import views

app_name="tasks_app"

urlpatterns = [

    path('', views.employee_dashboard, name='employee_dashboard'),

    
]
