"""
URL routing untuk halaman publik.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('artikel/', views.article_list, name='article_list'),
    path('artikel/<slug:slug>/', views.article_detail, name='article_detail'),
    path('tentang/', views.about_page, name='about'),
    path('kontak/', views.contact_page, name='contact'),
]
