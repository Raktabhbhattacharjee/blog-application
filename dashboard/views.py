from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blogs.models import Blog, Category, SocialLink


def dashboard(request):
    """
    Renders the Author Dashboard.
    Fetches the logged-in author's posts, or all posts in dev preview.
    """
    if request.user.is_authenticated:
        user_posts = Blog.objects.filter(author=request.user).select_related("category", "author")
        if not user_posts.exists() and not request.user.is_superuser:
            posts = Blog.objects.all().select_related("category", "author")
        else:
            posts = user_posts
    else:
        posts = Blog.objects.all().select_related("category", "author")

    context = {
        "posts": posts,
        "total_posts": posts.count(),
        "published_count": posts.filter(status="Published").count(),
        "draft_count": posts.filter(status="Draft").count(),
        "featured_count": posts.filter(is_featured=True).count(),
        "active_tab": "posts",
    }

    return render(request, "pages/dashboard/page_dashboard_author.html", context)


def admin_dashboard(request):
    """
    Renders the Staff/Admin Overview Dashboard.
    Protected: Only staff and superusers can access this view.
    Non-staff authors are redirected to the Author Workspace.
    """
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        return redirect("dashboard")
    total_posts = Blog.objects.count()
    published_count = Blog.objects.filter(status="Published").count()
    draft_count = Blog.objects.filter(status="Draft").count()
    featured_count = Blog.objects.filter(is_featured=True).count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    total_social_links = SocialLink.objects.filter(is_active=True).count()

    recent_posts = Blog.objects.select_related("category", "author").order_by("-created_at")[:7]

    # Calculate category distribution for progress bars
    category_stats = []
    for cat in Category.objects.all():
        count = Blog.objects.filter(category=cat).count()
        pct = round((count / total_posts * 100)) if total_posts > 0 else 0
        category_stats.append({
            "category": cat,
            "count": count,
            "percentage": pct,
        })

    # Sort categories by post count descending
    category_stats.sort(key=lambda x: x["count"], reverse=True)

    context = {
        "total_posts": total_posts,
        "published_count": published_count,
        "draft_count": draft_count,
        "featured_count": featured_count,
        "total_categories": total_categories,
        "total_users": total_users,
        "total_social_links": total_social_links,
        "recent_posts": recent_posts,
        "category_stats": category_stats,
        "active_tab": "admin_overview",
    }

    return render(request, "pages/dashboard/page_dashboard_admin.html", context)
