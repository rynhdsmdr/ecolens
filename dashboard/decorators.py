"""
Custom decorator untuk memastikan user adalah admin/staff.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator yang memastikan user sudah login dan merupakan staff/admin.
    Jika belum login, redirect ke halaman login.
    Jika bukan staff, redirect ke halaman utama.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Silakan login terlebih dahulu.')
            return redirect('dashboard:login')
        if not request.user.is_staff:
            messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
            return redirect('core:landing')
        return view_func(request, *args, **kwargs)
    return wrapper
