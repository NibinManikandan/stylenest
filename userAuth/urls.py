from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)




urlpatterns = [
    path('Userlogin/', views.user_Login, name ='Userlogin'),
    path('signup/',views.user_Signup, name ='signup'),
    path('otp_page/', views.verify_otp, name = 'otp_page'),
    path('resend/', views.send_otp_email, name ='resend'),
    path('logout/', views.Logout, name ='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='User_/password_reset.html'),name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='User_/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='User_/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='User_/password_reset_complete.html'),name='password_reset_complete'),
]
