from django.urls import path
from . import views

urlpatterns = [
    path("", views.stud_list, name="stud_list"),
    path("create/", views.stud_add, name="stud_add"),
    path("update/<int:id>/", views.stud_edit, name="stud_update"),
    path("delete/<int:id>/", views.stud_del, name="stud_delete"),
]
