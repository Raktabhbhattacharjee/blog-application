from django.shortcuts import render
from blogs.models import Blog


def home(request):
    """
    Renders the blog homepage.

    Note: `categories` is injected site-wide by blogs/context_processors.py,
    so it does not need to be added here.
    """

    # Newest first comes from Blog.Meta.ordering
    # select_related avoids a query per card for category/author
    published = Blog.objects.filter(status="Published").select_related("category", "author")

    context = {
        "featured_posts": published.filter(is_featured=True)[:4],
        "posts": published.filter(is_featured=False),
    }

    return render(request, "pages/blog/page_home.html", context)
