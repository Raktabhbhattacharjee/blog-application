from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count

from .models import Category, Blog, About, SocialLink, Comment
from .forms import CategoryForm, CommentForm


def home(request):
    """
    Renders the blog homepage with featured and recent published posts.
    Note: 'categories' is automatically injected globally by context_processors.py.

    NOTE: the '/' route is currently wired to blog_main.views.home, so this view
    is not reachable through blog_main/urls.py.
    """
    published = Blog.objects.filter(status="Published").select_related(
        "category", "author"
    )

    context = {
        # SELECT * FROM blogs_blog WHERE is_featured = True AND status = 'Published';
        "featured_posts": published.filter(is_featured=True),
        # SELECT * FROM blogs_blog WHERE is_featured = False AND status = 'Published';
        "posts": published.filter(is_featured=False),
    }

    return render(request, "pages/blog/page_home.html", context)


def post_by_category(request, category_id):
    """
    Renders all published posts under a specific category with like and comment counts.
    """
    category = get_object_or_404(Category, id=category_id)
    posts = (
        Blog.objects.filter(status="Published", category=category)
        .select_related("category", "author")
        .annotate(
            total_likes=Count("likes", distinct=True),
            total_comments=Count("comments", distinct=True),
        )
    )

    context = {
        "category": category,
        "posts": posts,
        "active_category_id": category.id,
    }
    return render(request, "pages/blog/page_category.html", context)


def post_detail(request, slug):
    """
    Renders a single published blog post matching the URL slug.
    """
    post = get_object_or_404(
        Blog.objects.select_related("category", "author"),
        slug=slug,
        status="Published",
    )
    context = {"post": post}
    return render(request, "pages/blog/page_post_detail.html", context)


def blogs(request, slug):
    """
    Single post detail view handling article display, like status, and comment submissions.
    """
    single_post = get_object_or_404(
        Blog.objects.select_related("category", "author"),
        slug__iexact=slug,
        status="Published",
    )

    # Handle Comment Submission
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to leave a response.")
            return redirect(f"/login/?next={request.path}")

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = single_post
            comment.save()
            messages.success(request, "Your response has been published!")
            return redirect("post_detail", slug=single_post.slug)
    else:
        comment_form = CommentForm()

    # Fetch comments (newest first)
    comments = single_post.comments.select_related("user").all()

    # Check if the logged-in user liked this post
    is_liked = False
    if request.user.is_authenticated:
        is_liked = single_post.likes.filter(id=request.user.id).exists()

    context = {
        "single_post": single_post,
        "active_category_id": single_post.category_id,
        "comments": comments,
        "comment_form": comment_form,
        "is_liked": is_liked,
        "likes_count": single_post.likes.count(),
        "comments_count": comments.count(),
    }
    return render(request, "pages/blog/page_blog_list.html", context)


@login_required
def toggle_like(request, pk):
    """
    Toggles the like status of a blog post for the authenticated user.
    """
    post = get_object_or_404(Blog, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("post_detail", slug=post.slug)



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

    return render(request, "pages/about.html", context)


# search functionality
def search(request):
    # 1. Grab the search keyword from the GET query parameters (?keyword=...)
    keyword = request.GET.get("keyword", "").strip()

    blogs = Blog.objects.none()  # Start with an empty QuerySet

    # 2. Pattern match using Q objects if a keyword was typed
    if keyword:
        blogs = (
            Blog.objects.filter(
                Q(title__icontains=keyword)
                | Q(short_description__icontains=keyword)
                | Q(blog_body__icontains=keyword)
                | Q(category__category_name__icontains=keyword),
                status="Published",
            )
            .select_related("category", "author")
            .annotate(
                total_likes=Count("likes", distinct=True),
                total_comments=Count("comments", distinct=True),
            )
            .distinct()
        )


    # 3. Package results and search term into context
    context = {
        "blogs": blogs,
        "keyword": keyword,
        "count": blogs.count(),
    }

    # 4. Render the template (matching your template folder 'blog/')
    return render(request, "pages/blog/page_search.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect(
            "dashboard"
            if (
                request.user.is_staff
                or request.user.groups.filter(name="Authors").exists()
            )
            else "home"
        )

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "pages/blog/page_register.html", context)