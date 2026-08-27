from django import forms
from blogs.models import Category


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
