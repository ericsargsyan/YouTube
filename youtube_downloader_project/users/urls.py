from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register_page"),
    path('', views.profile_page, name="profile_page"),
    path('login/', auth_views.LoginView.as_view(), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update_profile/', views.profile_update, name='profile_update'),
    path('logout_confirm/', views.logout, name='logout_page'),
]
