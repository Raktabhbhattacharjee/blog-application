from django import forms
from .models import Category, Comment


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
        labels = {
            "comment_text": "Leave a thoughtful response",
        }
        widgets = {
            "comment_text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-800 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition resize-y",
                    "placeholder": "What are your thoughts on this article? Join the discussion...",
                }
            )
        }