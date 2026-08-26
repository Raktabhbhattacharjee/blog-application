from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("admin-overview/", views.admin_dashboard, name="dashboard_admin"),
]