"""
Models untuk aplikasi core (halaman publik).
Berisi model Category, Article, dan ContactMessage.
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """Kategori artikel berita lingkungan."""

    name = models.CharField('Nama Kategori', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=120, unique=True, blank=True)
    icon = models.CharField(
        'Ikon (emoji)',
        max_length=10,
        default='📁',
        help_text='Gunakan emoji sebagai ikon kategori',
    )
    description = models.TextField('Deskripsi', blank=True, default='')
    created_at = models.DateTimeField('Dibuat', auto_now_add=True)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:article_list') + f'?category={self.slug}'

    @property
    def article_count(self):
        return self.articles.filter(status='published').count()


class Article(models.Model):
    """Artikel berita lingkungan."""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Diterbitkan'),
    ]

    title = models.CharField('Judul', max_length=255)
    slug = models.SlugField('Slug', max_length=280, unique=True, blank=True)
    excerpt = models.TextField(
        'Ringkasan',
        max_length=500,
        help_text='Ringkasan singkat artikel (maks 500 karakter)',
    )
    content = models.TextField('Konten')
    image = models.ImageField(
        'Gambar',
        upload_to='articles/%Y/%m/',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name='Kategori',
    )
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
    )
    is_featured = models.BooleanField('Artikel Unggulan', default=False)
    author = models.CharField('Penulis', max_length=100, default='Admin')
    views_count = models.PositiveIntegerField('Jumlah Dilihat', default=0)
    published_at = models.DateTimeField('Tanggal Publikasi', default=timezone.now)
    created_at = models.DateTimeField('Dibuat', auto_now_add=True)
    updated_at = models.DateTimeField('Diperbarui', auto_now=True)

    class Meta:
        verbose_name = 'Artikel'
        verbose_name_plural = 'Artikel'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:article_detail', kwargs={'slug': self.slug})


class ContactMessage(models.Model):
    """Pesan kontak dari pengunjung."""

    name = models.CharField('Nama', max_length=100)
    email = models.EmailField('Email')
    subject = models.CharField('Subjek', max_length=200)
    message = models.TextField('Pesan')
    is_read = models.BooleanField('Sudah Dibaca', default=False)
    created_at = models.DateTimeField('Dikirim', auto_now_add=True)

    class Meta:
        verbose_name = 'Pesan Kontak'
        verbose_name_plural = 'Pesan Kontak'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} - {self.name}'
