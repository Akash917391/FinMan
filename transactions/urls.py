from django.urls import path
from .views import *

urlpatterns = [
    path("", user_login, name="login"),
    path("dashboard/", dashboard , name="dashboard"),
    path("transaction/" , transaction , name="transaction"),
    path("delete/<int:id>/" , delete_transaction , name="delete_transaction"),
    # path("edit/<int:id>/", edit_transaction, name="edit_transaction"),
    path("register/", register, name="register"),
    path("logout/", user_logout, name="logout"),
    path("manage/" , manage , name="manage"),
    path("delete-category/<int:id>/",delete_category,name="delete_category"),
]