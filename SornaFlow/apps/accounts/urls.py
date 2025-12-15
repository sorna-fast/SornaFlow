from django.urls import path
from .views import LoginUserView, LogoutView

app_name = "accounts_app"  # Namespace for URL reversing

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),  # Login page route
    path('logout/', LogoutView.as_view(), name='logout'),   # Logout route
]
