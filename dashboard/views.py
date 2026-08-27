from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blogs.models import Blog, Category, SocialLink
from django.contrib import messages
from .forms import CategoryForm


@login_required
def dashboard(request):
    """
    Renders the Author Dashboard.
    Requires login. Fetches the logged-in author's posts.
    """
    user_posts = Blog.objects.filter(author=request.user).select_related(
        "category", "author"
    )
    if not user_posts.exists() and not request.user.is_superuser:
        posts = Blog.objects.all().select_related("category", "author")
    else:
        posts = user_posts

    context = {
        "posts": posts,
        "total_posts": posts.count(),
        "published_count": posts.filter(status="Published").count(),
        "draft_count": posts.filter(status="Draft").count(),
        "featured_count": posts.filter(is_featured=True).count(),
        "active_tab": "posts",
    }

    return render(request, "pages/dashboard/page_dashboard_author.html", context)


@login_required
def admin_dashboard(request):
    """
    Renders the Staff/Admin Overview Dashboard.
    Protected: Requires login, and only staff and superusers can access this view.
    Non-staff authors are redirected to the Author Workspace.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("dashboard")
    total_posts = Blog.objects.count()
    published_count = Blog.objects.filter(status="Published").count()
    draft_count = Blog.objects.filter(status="Draft").count()
    featured_count = Blog.objects.filter(is_featured=True).count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    total_social_links = SocialLink.objects.filter(is_active=True).count()

    recent_posts = Blog.objects.select_related("category", "author").order_by(
        "-created_at"
    )[:7]

    # Calculate category distribution for progress bars
    category_stats = []
    for cat in Category.objects.all():
        count = Blog.objects.filter(category=cat).count()
        pct = round((count / total_posts * 100)) if total_posts > 0 else 0
        category_stats.append(
            {
                "category": cat,
                "count": count,
                "percentage": pct,
            }
        )

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


@login_required
def categories(request):
    """
    Renders the Categories Table on the dashboard (Item 48).
    """
    category_list = Category.objects.all().order_by("-created_at")
    context = {
        "categories": category_list,
        "active_tab": "categories",
    }
    return render(request, "pages/dashboard/page_categories.html", context)


@login_required
def add_category(request):
    """
    Renders and handles the Add Category form (Items 49 & 50).
    """

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(
                request, f"Category '{category.category_name}' created successfully!"
            )
            return redirect("categories")
    else:
        form = CategoryForm()

    context = {
        "form": form,
        "active_tab": "categories",
    }
    return render(request, "pages/dashboard/page_add_category.html", context)
