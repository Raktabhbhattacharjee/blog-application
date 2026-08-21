from django.urls import path
from . import views

urlpatterns = [
    # categoru url basiclly when i want to do is is someone clicks on this /category/1
    path(
        'category/<int:category_id>/',
        views.post_by_category,
        name='post_by_category'
    ),
    
    # Single Post Detail Route: Matches URL slugs (e.g., /my-first-post/)
    # Equivalent to FastAPI: @app.get("/{slug:str}")
    path(
        '<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),
]