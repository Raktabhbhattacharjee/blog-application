from django.shortcuts import render, get_object_or_404
from .models import Blog, Category

def post_by_category(request, category_id):
    # Fetch category object or return 404
    category = get_object_or_404(Category, id=category_id)

    # Filter published posts for this category
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


# --- ADD THIS FUNCTION TO COMPLETE STEP 2 ---
def post_detail(request, slug):
    # Fetch the post matching the slug from the URL
    post = get_object_or_404(Blog, slug=slug, status="Published")

    context = {
        "post": post,
    }

    return render(
        request,
        "blog/post_detail.html",
        context
    )