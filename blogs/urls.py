from django.urls import path
from . import views

urlpatterns = [
    # Matches: /about/
    path("about/", views.about, name="about"),
    # Matches: /category/1/
    path("<int:category_id>/", views.post_by_category, name="post_by_category"),
    path("search/", views.search, name="search"),
]