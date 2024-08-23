from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('activation_prompt/<int:user_id>/', views.activation_prompt, name='activation_prompt'),
    path('resend_activation_email/', views.resend_activation_email, name='resend_activation_email'),
    path('activate_account_page/', views.activate_account_page, name='activate_account_page'),

]
