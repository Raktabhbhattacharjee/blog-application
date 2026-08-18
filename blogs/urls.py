from django.urls import path
from . import views

urlpatterns = [
    # Category URL (Existing)
    path(
        '<int:category_id>/',
        views.post_by_category,
        name='post_by_category'
    ),
    
    # Single Post Detail URL (ADD THIS)
    path(
        '<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),
]