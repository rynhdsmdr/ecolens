"""
Forms untuk aplikasi core.
"""

from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Form kontak untuk pengunjung."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama lengkap Anda',
                'id': 'contact-name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@contoh.com',
                'id': 'contact-email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subjek pesan',
                'id': 'contact-subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis pesan Anda di sini...',
                'rows': 5,
                'id': 'contact-message',
            }),
        }
