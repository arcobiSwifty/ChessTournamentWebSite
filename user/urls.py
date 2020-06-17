from django.urls import path

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .views import SignupView

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('accounts/logout', auth_views.LogoutView.as_view()),
    path('accounts/register', SignupView.as_view()),
]
