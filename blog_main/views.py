from django.shortcuts import render
from django.db.models import Count
from blogs.models import Blog


def home(request):
    """
    Renders the blog homepage.

    Note: `categories` is injected site-wide by blogs/context_processors.py,
    so it does not need to be added here.
    """

    # select_related avoids queries for category/author
    # annotate calculates total_likes and total_comments in 1 query (kills N+1 problem)
    published = (
        Blog.objects.filter(status="Published")
        .select_related("category", "author")
        .annotate(
            total_likes=Count("likes", distinct=True),
            total_comments=Count("comments", distinct=True),
        )
    )

    context = {
        "featured_posts": published.filter(is_featured=True)[:4],
        "posts": published.filter(is_featured=False),
    }

    return render(request, "pages/blog/page_home.html", context)

