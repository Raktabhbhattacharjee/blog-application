from django.shortcuts import render, get_object_or_404
from .models import Category, Blog, About, SocialLink


def home(request):
    """
    Renders the blog homepage with featured and recent published posts.
    Note: 'categories' is automatically injected globally by context_processors.py.

    NOTE: the '/' route is currently wired to blog_main.views.home, so this view
    is not reachable through blog_main/urls.py.
    """
    published = Blog.objects.filter(status="Published").select_related("category", "author")

    context = {
        # SELECT * FROM blogs_blog WHERE is_featured = True AND status = 'Published';
        "featured_posts": published.filter(is_featured=True),
        # SELECT * FROM blogs_blog WHERE is_featured = False AND status = 'Published';
        "posts": published.filter(is_featured=False),
    }

    return render(request, "blog/home.html", context)


def post_by_category(request, category_id):
    """
    Renders all published posts under a specific category.
    """
    # 1. Fetch category object or immediately raise Http404 (renders 404.html)
    category = get_object_or_404(Category, id=category_id)

    # 2. SELECT * FROM blogs_blog WHERE status='Published' AND category_id=category_id;
    posts = (
        Blog.objects
        .filter(status="Published", category=category)
        .select_related("category", "author")
    )

    context = {
        "category": category,
        "posts": posts,
        # lets base.html highlight the matching navbar link
        "active_category_id": category.id,
    }

    return render(
        request,
        "blog/post_by_category.html",
        context
    )


def post_detail(request, slug):
    """
    Renders a single published blog post matching the URL slug.

    NOTE: the '<slug:slug>/' route is currently wired to blogs.views.blogs, so
    this view is not reachable through blog_main/urls.py.
    """
    # SELECT * FROM blogs_blog WHERE slug=slug AND status='Published' LIMIT 1;
    post = get_object_or_404(
        Blog.objects.select_related("category", "author"),
        slug=slug,
        status="Published",
    )

    context = {
        "post": post,
    }

    return render(
        request,
        "blog/post_detail.html",
        context
    )


def blogs(request, slug):
    """
    Single post detail view used by the 'post_detail' URL name.
    """
    # 'iexact' ignores uppercase/lowercase differences
    single_post = get_object_or_404(
        Blog.objects.select_related("category", "author"),
        slug__iexact=slug,
        status="Published",
    )

    context = {
        "single_post": single_post,
        "active_category_id": single_post.category_id,
    }
    return render(request, "blog/blogs.html", context)


def about(request):
    """
    Renders the About Us page with author details and active social media links.
    """
    about_info = About.objects.first()
    social_links = SocialLink.objects.filter(is_active=True)

    context = {
        "about": about_info,
        "social_links": social_links,
    }

    return render(request, "about.html", context)