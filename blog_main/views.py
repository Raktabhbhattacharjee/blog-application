# blog_main/views.py
from django.shortcuts import render
from blogs.models import Category
def home(request):
    """
    Renders the blog homepage.
    FastAPI comparison: Equivalent to a path function returning HTMLResponse via Jinja2.
    """
    # fetcting the categories from the database 
    categories =Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'blog/home.html',context)