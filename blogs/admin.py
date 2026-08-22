from django.contrib import admin
from .models import Category, Blog, About, SocialLink


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "author", "status", "is_featured")
    search_fields = ("id", "title", "category__category_name", "status")
    list_editable = ('is_featured',)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('platform',)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')

    # Prevents adding multiple About objects from admin if you only want 1 profile/about record
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)