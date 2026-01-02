from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("list", emp_list, name="emp_list"),
    path("add", emp_create, name="emp_add"),
    path("edit/<int:pk>", emp_edit, name="emp_edit"),
    path("del/<int:pk>", emp_del, name="emp_del"),
    path("signup/", signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="employee/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
