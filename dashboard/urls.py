"""
URL routing untuk dashboard admin.
Semua URL di-prefix /admin-panel/.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard Home
    path('', views.dashboard_home, name='home'),

    # CRUD Artikel
    path('artikel/', views.article_list, name='article_list'),
    path('artikel/tambah/', views.article_create, name='article_create'),
    path('artikel/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('artikel/<int:pk>/hapus/', views.article_delete, name='article_delete'),

    # CRUD Kategori
    path('kategori/', views.category_list, name='category_list'),
    path('kategori/tambah/', views.category_create, name='category_create'),
    path('kategori/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('kategori/<int:pk>/hapus/', views.category_delete, name='category_delete'),

    # Manajemen Pesan
    path('pesan/', views.message_list, name='message_list'),
    path('pesan/<int:pk>/', views.message_detail, name='message_detail'),
    path('pesan/<int:pk>/hapus/', views.message_delete, name='message_delete'),
]
