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

# one category can have many blog posts but a blog post can belong to only one category
# eg: sports can have cricket, football, volleyball
# eg: cricket belongs to sports
# eg: demon slayer belongs to anime

# creating blog models  
class Blog(models.Model):
    title = models.CharField(max_length=100)
    # unique: the detail URL looks a post up by slug alone, so duplicates
    # would make get_object_or_404() raise MultipleObjectsReturned
    slug = models.SlugField(max_length=150, unique=True)
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
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # newest first, so "Recent posts" listings are actually recent
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()


# comment model
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"



# about us and social link models 
class SocialLink(models.Model):
    platform = models.CharField(max_length=50)  # e.g., GitHub, Twitter, LinkedIn
    url = models.URLField()
    icon_class = models.CharField(
        max_length=50, 
        help_text="Bootstrap or FontAwesome icon class, e.g., 'bi-github'"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.platform


class About(models.Model):
    title = models.CharField(max_length=200, default="About Us")
    content = models.TextField()
    profile_image = models.ImageField(upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About"

    def __str__(self):
        return self.title