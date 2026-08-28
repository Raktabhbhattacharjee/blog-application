from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from blogs.models import Blog, Category, SocialLink
from django.contrib import messages
from .forms import CategoryForm, BlogPostForm




@login_required
def dashboard(request):
    """
    Renders the Author Dashboard.
    Requires login. Fetches the logged-in author's posts.
    """
    if request.user.is_staff or request.user.is_superuser:
        posts = Blog.objects.all().select_related("category", "author")
    else:
        posts = Blog.objects.filter(author=request.user).select_related("category", "author")


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


@login_required
def edit_category(request, pk):
    """
    Renders and handles editing an existing Category (Item 51).
    """
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Category '{category.category_name}' updated successfully!"
            )
            return redirect("categories")
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category,
        "active_tab": "categories",
    }
    return render(request, "pages/dashboard/page_edit_category.html", context)


@login_required
def delete_category(request, pk):
    """
    Deletes an existing Category.
    """
    category = get_object_or_404(Category, pk=pk)
    category_name = category.category_name
    category.delete()
    messages.success(request, f"Category '{category_name}' was deleted successfully.")
    return redirect("categories")


# ==========================================
# POST / ARTICLE CRUD OPERATIONS
# ==========================================


@login_required
def add_post(request):
    """
    Creates a new Blog article.
    Handles image uploads, auto-generates a unique slug, and assigns the logged-in author.
    """
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Auto-generate a unique slug from the title
            base_slug = slugify(post.title)
            slug = base_slug
            count = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            post.slug = slug

            post.save()
            messages.success(request, f"Article '{post.title}' created successfully!")
            return redirect("dashboard")
    else:
        form = BlogPostForm()

    context = {
        "form": form,
        "active_tab": "posts",
    }
    return render(request, "pages/dashboard/page_add_post.html", context)


@login_required
def edit_post(request, pk):
    """
    Edits an existing Blog article.
    Ensures authors can only edit their own posts (staff/superusers can edit any post).
    """
    if request.user.is_staff or request.user.is_superuser:
        post = get_object_or_404(Blog, pk=pk)
    else:
        post = get_object_or_404(Blog, pk=pk, author=request.user)

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f"Article '{post.title}' updated successfully!")
            return redirect("dashboard")
    else:
        form = BlogPostForm(instance=post)

    context = {
        "form": form,
        "post": post,
        "active_tab": "posts",
    }
    return render(request, "pages/dashboard/page_edit_post.html", context)


@login_required
def delete_post(request, pk):
    """
    Deletes an existing Blog article.
    Ensures authors can only delete their own posts (staff/superusers can delete any post).
    """
    if request.user.is_staff or request.user.is_superuser:
        post = get_object_or_404(Blog, pk=pk)
    else:
        post = get_object_or_404(Blog, pk=pk, author=request.user)

    title = post.title
    post.delete()
    messages.success(request, f"Article '{title}' was deleted successfully.")
    return redirect("dashboard")


@login_required
def toggle_post_status(request, pk):
    """
    Toggles the publication status of an article between 'Draft' and 'Published'.
    """
    if request.user.is_staff or request.user.is_superuser:
        post = get_object_or_404(Blog, pk=pk)
    else:
        post = get_object_or_404(Blog, pk=pk, author=request.user)

    if post.status == "Draft":
        post.status = "Published"
    else:
        post.status = "Draft"

    post.save()
    messages.success(
        request, f"Article status for '{post.title}' updated to '{post.status}'."
    )
    return redirect("dashboard")


