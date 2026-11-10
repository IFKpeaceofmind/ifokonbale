from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('register/', views.register, name='register'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]