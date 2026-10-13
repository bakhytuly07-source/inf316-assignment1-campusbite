from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("after-login/", views.after_login, name="after_login"),
    path("stations/", views.stations, name="stations"),
    path("staff/", views.staff_board, name="staff_board"),
    path("manage/", views.admin_menu, name="admin_menu"),
]
