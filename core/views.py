"""
Views untuk halaman publik.
Landing page, daftar artikel, detail artikel, about, dan kontak.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from .models import Article, Category, ContactMessage
from .forms import ContactForm


def landing_page(request):
    """Halaman utama / landing page."""
    featured_articles = Article.objects.filter(
        status='published', is_featured=True
    ).select_related('category')[:3]

    latest_articles = Article.objects.filter(
        status='published'
    ).select_related('category')[:6]

    categories = Category.objects.all()

    # Statistik
    stats = {
        'articles': Article.objects.filter(status='published').count(),
        'categories': Category.objects.count(),
        'readers': Article.objects.filter(status='published').values_list(
            'views_count', flat=True
        ),
    }
    stats['total_views'] = sum(stats['readers']) if stats['readers'] else 0

    context = {
        'featured_articles': featured_articles,
        'latest_articles': latest_articles,
        'categories': categories,
        'stats': stats,
    }
    return render(request, 'core/landing.html', context)


def article_list(request):
    """Daftar semua artikel dengan paginasi dan filter."""
    articles = Article.objects.filter(
        status='published'
    ).select_related('category')

    # Filter berdasarkan kategori
    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=active_category)

    # Pencarian
    query = request.GET.get('q', '')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        )

    # Paginasi
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'active_category': active_category,
        'query': query,
    }
    return render(request, 'core/articles.html', context)


def article_detail(request, slug):
    """Detail satu artikel."""
    article = get_object_or_404(Article, slug=slug, status='published')

    # Increment view count
    article.views_count += 1
    article.save(update_fields=['views_count'])

    # Artikel terkait (kategori sama)
    related_articles = Article.objects.filter(
        status='published',
        category=article.category,
    ).exclude(pk=article.pk).select_related('category')[:3]

    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'core/article_detail.html', context)


def about_page(request):
    """Halaman tentang EcoLens."""
    stats = {
        'articles': Article.objects.filter(status='published').count(),
        'categories': Category.objects.count(),
    }
    return render(request, 'core/about.html', {'stats': stats})


def contact_page(request):
    """Halaman kontak dengan form pengiriman pesan."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Pesan Anda berhasil dikirim! Kami akan segera merespons.'
            )
            return redirect('core:contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
