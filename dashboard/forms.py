"""
Forms untuk dashboard admin.
"""

from django import forms
from core.models import Article, Category


class ArticleForm(forms.ModelForm):
    """Form untuk membuat dan mengedit artikel."""

    class Meta:
        model = Article
        fields = [
            'title', 'excerpt', 'content', 'image',
            'category', 'status', 'is_featured', 'author', 'published_at',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul artikel',
                'id': 'article-title',
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ringkasan singkat artikel...',
                'rows': 3,
                'id': 'article-excerpt',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis konten artikel di sini...',
                'rows': 12,
                'id': 'article-content',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'article-image',
                'accept': 'image/*',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'article-category',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'article-status',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'article-featured',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama penulis',
                'id': 'article-author',
            }),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'id': 'article-published-at',
            }),
        }


class CategoryForm(forms.ModelForm):
    """Form untuk membuat dan mengedit kategori."""

    class Meta:
        model = Category
        fields = ['name', 'icon', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama kategori',
                'id': 'category-name',
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '📁',
                'id': 'category-icon',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi kategori...',
                'rows': 3,
                'id': 'category-description',
            }),
        }
