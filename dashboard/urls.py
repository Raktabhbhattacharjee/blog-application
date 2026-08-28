from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("admin-overview/", views.admin_dashboard, name="dashboard_admin"),
    
    # Category Management
    path("categories/", views.categories, name="categories"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/edit/<int:pk>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
    
    # Post / Article Management
    path("posts/add/", views.add_post, name="add_post"),
    path("posts/edit/<int:pk>/", views.edit_post, name="edit_post"),
    path("posts/delete/<int:pk>/", views.delete_post, name="delete_post"),
    path("posts/toggle-status/<int:pk>/", views.toggle_post_status, name="toggle_post_status"),
]


