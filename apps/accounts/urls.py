from django.urls import path
from .views import LoginView,RegisterView,VerifyEmailView,ProfileView,GoogleLoginView,ProfileUpdateView,ForgotPasswordView,ResetPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('login/',LoginView.as_view(),name="login"),
    path('register/',RegisterView.as_view(),name="register"),
    path('refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('verify-email/<uidb64>/<token>/',VerifyEmailView.as_view(),name="verify_email"),
    path('google/',GoogleLoginView.as_view(),name="google_login"),
    path('profile/',ProfileView.as_view(),name="profile"),
    path('profile-update/',ProfileUpdateView.as_view(),name="profile"),
    path('forgot-password/',ForgotPasswordView.as_view(),name="forgot-password"),
    path('reset-password/',ResetPasswordView.as_view(),name="forgot-password"),
]