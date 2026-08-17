from django.shortcuts import render
from blogs.models import Category, Blog


def home(request):
    """
    Renders the blog homepage.
    """

    # Fetch featured and published blog posts
    featured_posts = Blog.objects.filter(
        is_featured=True,
        status="Published"
    )

    # Fetch all categories
    categories = Category.objects.all()

    # Fetch non-featured and published blog posts
    posts = Blog.objects.filter(
        is_featured=False,
        status="Published"
    )

    context = {
        "categories": categories,
        "featured_posts": featured_posts,
        "posts": posts,
    }

    return render(request, "blog/home.html", context)