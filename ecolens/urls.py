"""
URL configuration for ecolens project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django built-in admin (backup)
    path('django-admin/', admin.site.urls),

    # Custom dashboard admin
    path('admin-panel/', include('dashboard.urls')),

    # Public pages
    path('', include('core.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
