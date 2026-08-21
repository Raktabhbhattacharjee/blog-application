from .models import Category


def get_categories(request):
    """
    Global Context Processor for Blog Categories.
    
    Fetches all categories from the database and injects them into
    the template context site-wide (available across all views/pages).
    """
    categories = Category.objects.all()
    
    return {
        'categories': categories
    }
    
# categories = Category.objects.all()

# meaning 
# SELECT * FROM blogs_category; 