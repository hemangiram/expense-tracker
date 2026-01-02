from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.dashboard, name="expense_list"),
    path("del/<int:pk>", views.delete_expense, name="delete_expense"),
    path("edit/<int:pk>/", views.edit_transaction, name="edit_expense"),  # New URL
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
]
