from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import Category, Blog, About, SocialLink
from .forms import CategoryForm

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
    Renders all published posts under a specific category.
    """
    # 1. Fetch category object or immediately raise Http404 (renders 404.html)
    category = get_object_or_404(Category, id=category_id)

    # 2. SELECT * FROM blogs_blog WHERE status='Published' AND category_id=category_id;
    posts = Blog.objects.filter(status="Published", category=category).select_related(
        "category", "author"
    )

    context = {
        "category": category,
        "posts": posts,
        # lets base.html highlight the matching navbar link
        "active_category_id": category.id,
    }

    return render(request, "pages/blog/page_category.html", context)


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

    return render(request, "pages/blog/page_post_detail.html", context)


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
    return render(request, "pages/blog/page_blog_list.html", context)


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