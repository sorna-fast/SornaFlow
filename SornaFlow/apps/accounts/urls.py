from django.urls import path
from .views import LoginUserView, LogoutView
app_name="accounts_app"
urlpatterns = [
    path('login/',LoginUserView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
]