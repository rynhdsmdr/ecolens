"""
Views untuk dashboard admin.
CRUD Artikel, Kategori, dan Manajemen Pesan.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from core.models import Article, Category, ContactMessage
from .forms import ArticleForm, CategoryForm
from .decorators import admin_required


# ─── Authentication ───────────────────────────────────────────────

def login_view(request):
    """Halaman login admin."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:home')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, f'Selamat datang, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next', 'dashboard:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Akun Anda tidak memiliki akses admin.')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'dashboard/login.html')


@login_required
def logout_view(request):
    """Logout admin."""
    logout(request)
    messages.info(request, 'Anda telah berhasil logout.')
    return redirect('core:landing')


# ─── Dashboard Home ───────────────────────────────────────────────

@admin_required
def dashboard_home(request):
    """Halaman utama dashboard dengan statistik."""
    context = {
        'total_articles': Article.objects.count(),
        'published_articles': Article.objects.filter(status='published').count(),
        'draft_articles': Article.objects.filter(status='draft').count(),
        'total_categories': Category.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_articles': Article.objects.select_related('category')[:5],
        'recent_messages': ContactMessage.objects.filter(is_read=False)[:5],
    }
    return render(request, 'dashboard/home.html', context)


# ─── CRUD Artikel ─────────────────────────────────────────────────

@admin_required
def article_list(request):
    """Daftar semua artikel (admin)."""
    articles = Article.objects.select_related('category').all()

    # Pencarian
    query = request.GET.get('q', '')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Filter status
    status = request.GET.get('status', '')
    if status in ('draft', 'published'):
        articles = articles.filter(status=status)

    context = {
        'articles': articles,
        'query': query,
        'status_filter': status,
    }
    return render(request, 'dashboard/articles/list.html', context)


@admin_required
def article_create(request):
    """Buat artikel baru."""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Artikel "{article.title}" berhasil dibuat!')
            return redirect('dashboard:article_list')
    else:
        form = ArticleForm()

    return render(request, 'dashboard/articles/form.html', {
        'form': form,
        'title': 'Tambah Artikel Baru',
        'submit_text': 'Simpan Artikel',
    })


@admin_required
def article_edit(request, pk):
    """Edit artikel yang sudah ada."""
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f'Artikel "{article.title}" berhasil diperbarui!')
            return redirect('dashboard:article_list')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'dashboard/articles/form.html', {
        'form': form,
        'article': article,
        'title': 'Edit Artikel',
        'submit_text': 'Perbarui Artikel',
    })


@admin_required
def article_delete(request, pk):
    """Hapus artikel."""
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        title = article.title
        article.delete()
        messages.success(request, f'Artikel "{title}" berhasil dihapus!')
        return redirect('dashboard:article_list')

    return render(request, 'dashboard/articles/delete.html', {
        'article': article,
    })


# ─── CRUD Kategori ────────────────────────────────────────────────

@admin_required
def category_list(request):
    """Daftar semua kategori."""
    categories = Category.objects.all()
    return render(request, 'dashboard/categories/list.html', {
        'categories': categories,
    })


@admin_required
def category_create(request):
    """Buat kategori baru."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Kategori "{category.name}" berhasil dibuat!')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()

    return render(request, 'dashboard/categories/form.html', {
        'form': form,
        'title': 'Tambah Kategori Baru',
        'submit_text': 'Simpan Kategori',
    })


@admin_required
def category_edit(request, pk):
    """Edit kategori."""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Kategori "{category.name}" berhasil diperbarui!')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/categories/form.html', {
        'form': form,
        'category': category,
        'title': 'Edit Kategori',
        'submit_text': 'Perbarui Kategori',
    })


@admin_required
def category_delete(request, pk):
    """Hapus kategori."""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Kategori "{name}" berhasil dihapus!')
        return redirect('dashboard:category_list')

    return render(request, 'dashboard/categories/delete.html', {
        'category': category,
    })


# ─── Manajemen Pesan ──────────────────────────────────────────────

@admin_required
def message_list(request):
    """Daftar semua pesan masuk."""
    msg_messages = ContactMessage.objects.all()

    # Filter status baca
    read_filter = request.GET.get('read', '')
    if read_filter == 'unread':
        msg_messages = msg_messages.filter(is_read=False)
    elif read_filter == 'read':
        msg_messages = msg_messages.filter(is_read=True)

    context = {
        'contact_messages': msg_messages,
        'read_filter': read_filter,
    }
    return render(request, 'dashboard/messages/list.html', context)


@admin_required
def message_detail(request, pk):
    """Detail pesan & mark as read."""
    msg = get_object_or_404(ContactMessage, pk=pk)

    # Mark as read
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])

    return render(request, 'dashboard/messages/detail.html', {
        'msg': msg,
    })


@admin_required
def message_delete(request, pk):
    """Hapus pesan."""
    msg = get_object_or_404(ContactMessage, pk=pk)

    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Pesan berhasil dihapus!')
        return redirect('dashboard:message_list')

    return render(request, 'dashboard/messages/delete.html', {
        'msg': msg,
    })
