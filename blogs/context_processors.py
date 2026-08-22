from .models import Category, SocialLink


def get_categories(request):
    """
    Global Context Processor for Blog Categories and Social Links.

    Fetches all categories and active social links from the database and
    injects them into the template context site-wide (available across all
    views/pages).
    """
    categories = Category.objects.all()
    social_links = SocialLink.objects.filter(is_active=True)

    return {
        'categories': categories,
        'social_links': social_links,
    }
    
# categories = Category.objects.all()

# meaning 
# SELECT * FROM blogs_category; 