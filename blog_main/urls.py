# blog_main/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from blogs import views as BlogsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth routes
    path('login/', auth_views.LoginView.as_view(template_name="pages/blog/page_login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', BlogsView.register, name='register'),

    # Category URLs
    path('category/', include('blogs.urls')),

    # Single Post URL — UPDATED NAME TO 'post_detail'
     path("dashboard/", include("dashboard.urls")),
    path('<slug:slug>/', BlogsView.blogs, name='post_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)