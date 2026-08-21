from django.shortcuts import render, get_object_or_404
from .models import Blog, Category


def home(request):
    """
    Renders the blog homepage with featured and recent published posts.
    Note: 'categories' is automatically injected globally by context_processors.py.
    """
    # SELECT * FROM blogs_blog WHERE is_featured = True AND status = 'Published';
    featured_posts = Blog.objects.filter(is_featured=True, status="Published")
    
    # SELECT * FROM blogs_blog WHERE is_featured = False AND status = 'Published';
    posts = Blog.objects.filter(is_featured=False, status="Published")

    context = {
        "featured_posts": featured_posts,
        "posts": posts,
    }

    return render(request, "blog/home.html", context)


def post_by_category(request, category_id):
    """
    Renders all published posts under a specific category.
    """
    # 1. Fetch category object or immediately raise Http404 (renders 404.html)
    category = get_object_or_404(Category, id=category_id)

    # 2. SELECT * FROM blogs_blog WHERE status='Published' AND category_id=category_id;
    posts = Blog.objects.filter(
        status="Published",
        category=category
    )

    context = {
        "category": category,
        "posts": posts,
    }

    return render(
        request,
        "blog/post_by_category.html",
        context
    )


def post_detail(request, slug):
    """
    Renders a single published blog post matching the URL slug.
    """
    # SELECT * FROM blogs_blog WHERE slug=slug AND status='Published' LIMIT 1;
    post = get_object_or_404(Blog, slug=slug, status="Published")

    context = {
        "post": post,
    }

    return render(
        request,
        "blog/post_detail.html",
        context
    )