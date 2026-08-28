from django import forms
from blogs.models import Category, Blog


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("category_name",)
        labels = {
            "category_name": "Category Name",
        }
        widgets = {
            "category_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition",
                    "placeholder": "e.g. Technology, AI & Data, Web Dev, Mobile",
                    "autocomplete": "off",
                }
            )
        }


class BlogPostForm(forms.ModelForm):
    feature_image = forms.ImageField(
        required=False,
        label="Cover / Feature Image",
        widget=forms.FileInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition cursor-pointer",
            }
        ),
    )

    class Meta:
        model = Blog
        fields = (
            "title",
            "category",
            "feature_image",
            "short_description",
            "blog_body",
            "status",
            "is_featured",
        )
        labels = {
            "title": "Article Title",
            "category": "Category / Topic",
            "feature_image": "Cover / Feature Image",
            "short_description": "Short Summary / Subtitle",
            "blog_body": "Article Content",
            "status": "Publication Status",
            "is_featured": "Feature this article on Homepage",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition",
                    "placeholder": "Enter an engaging, descriptive title...",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition",
                }
            ),
            "feature_image": forms.FileInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition cursor-pointer",
                }
            ),
            "short_description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition",
                    "placeholder": "Brief 1-2 sentence overview shown in article previews and cards...",
                }
            ),
            "blog_body": forms.Textarea(
                attrs={
                    "rows": 10,
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition font-mono leading-relaxed",
                    "placeholder": "Write your full article body here...",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition",
                }
            ),
            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500 transition cursor-pointer",
                }
            ),
        }
