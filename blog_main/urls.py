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
    path('login/', auth_views.LoginView.as_view(template_name="pages/blog/page_login.html", redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', BlogsView.register, name='register'),

    # Category URLs
    path('category/', include('blogs.urls')),

    # Dashboard URLs
    path("dashboard/", include("dashboard.urls")),

    # Like / Reaction URL
    path("post/<int:pk>/like/", BlogsView.toggle_like, name="toggle_like"),

    # Single Post Detail URL
    path('<slug:slug>/', BlogsView.blogs, name='post_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)