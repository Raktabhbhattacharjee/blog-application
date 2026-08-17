from django.db import models
from django.contrib.auth.models import User


# creating Categroy models
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    # it returns categories name
    def __str__(self):
        return self.category_name

# just liike enum in fastapi 
STATUS_CHOICES = (("Draft", "Draft"), ("Published", "Published"))


# creating blog models
class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_image = models.ImageField(upload_to="blog/uploads/%Y/%m/%d")
    short_description = models.TextField(max_length=500)
    blog_body = models.TextField(max_length=2000)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft",
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title