# 🌱 EcoLens — Portal Berita & Informasi Lingkungan

EcoLens adalah aplikasi web modern untuk portal berita dan informasi lingkungan hidup. Dibangun dengan Django 5.x dan dirancang untuk memudahkan admin dalam mengelola artikel, kategori, dan pesan dari pengunjung.

## 🎯 Fitur Utama

### 👥 Untuk Pengunjung
- 📰 **Landing Page** — Halaman beranda dengan featured articles dan statistik
- 📚 **Daftar Artikel** — Browse semua artikel dengan paginasi dan filter kategori
- 🔍 **Search Artikel** — Cari artikel berdasarkan judul, ringkasan, atau konten
- 📖 **Detail Artikel** — Baca artikel lengkap dengan artikel terkait
- ℹ️ **Halaman About** — Informasi tentang EcoLens
- 💬 **Hubungi Kami** — Form kontak untuk mengirim pesan

### 🛠️ Untuk Admin
- 🔐 **Custom Admin Panel** — Dashboard admin khusus (bukan Django admin)
- 📝 **Manajemen Artikel** — CRUD (Create, Read, Update, Delete) artikel
- 🏷️ **Manajemen Kategori** — Kelola kategori artikel
- 💌 **Kelola Pesan** — Baca, tandai, dan hapus pesan dari pengunjung
- 📊 **Dashboard Stats** — Lihat statistik jumlah artikel, kategori, dan pesan

## 🛠️ Tech Stack

- **Backend**: Django 5.1+
- **Database**: SQLite (built-in, tidak perlu setup)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Image Handling**: Pillow 10.0+
- **Auto Cleanup**: django-cleanup 8.0+ (auto-delete media files)

## 📦 Instalasi & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd uas
```

### 2. Buat Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Buat Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Ikuti instruksi untuk membuat username, email, dan password admin.

### 6. Jalankan Development Server
```bash
python manage.py runserver
```

Server akan berjalan di `http://127.0.0.1:8000/`

## 🌐 Navigasi Website

| URL | Fungsi |
|-----|--------|
| `/` | Landing page |
| `/artikel/` | Daftar semua artikel |
| `/artikel/<slug>/` | Detail artikel |
| `/tentang/` | Halaman tentang EcoLens |
| `/kontak/` | Form kontak |
| `/admin-panel/login/` | Login admin |
| `/admin-panel/` | Dashboard admin |
| `/django-admin/` | Django admin (backup) |

## 📋 API Routes Dashboard Admin

Semua route di-prefix dengan `/admin-panel/` dan memerlukan login.

### Authentication
- `GET /admin-panel/login/` — Halaman login
- `GET /admin-panel/logout/` — Logout

### Dashboard
- `GET /admin-panel/` — Dashboard home dengan statistik

### CRUD Artikel
- `GET /admin-panel/artikel/` — Daftar artikel (dengan search & filter)
- `GET /admin-panel/artikel/tambah/` — Form tambah artikel
- `POST /admin-panel/artikel/tambah/` — Simpan artikel baru
- `GET /admin-panel/artikel/<id>/edit/` — Form edit artikel
- `POST /admin-panel/artikel/<id>/edit/` — Update artikel
- `GET /admin-panel/artikel/<id>/hapus/` — Konfirmasi hapus
- `POST /admin-panel/artikel/<id>/hapus/` — Hapus artikel

### CRUD Kategori
- `GET /admin-panel/kategori/` — Daftar kategori
- `GET /admin-panel/kategori/tambah/` — Form tambah kategori
- `POST /admin-panel/kategori/tambah/` — Simpan kategori
- `GET /admin-panel/kategori/<id>/edit/` — Form edit kategori
- `POST /admin-panel/kategori/<id>/edit/` — Update kategori
- `GET /admin-panel/kategori/<id>/hapus/` — Konfirmasi hapus
- `POST /admin-panel/kategori/<id>/hapus/` — Hapus kategori

### Manajemen Pesan
- `GET /admin-panel/pesan/` — Daftar pesan (dengan filter read/unread)
- `GET /admin-panel/pesan/<id>/` — Detail pesan (auto-mark as read)
- `GET /admin-panel/pesan/<id>/hapus/` — Konfirmasi hapus pesan
- `POST /admin-panel/pesan/<id>/hapus/` — Hapus pesan

## 📁 Struktur Folder

```
uas/
├── manage.py                          # Django management utility
├── requirements.txt                   # Python dependencies
├── README.md                          # Dokumentasi ini
├── db.sqlite3                         # Database (auto-created)
│
├── ecolens/                           # Project configuration
│   ├── __init__.py
│   ├── settings.py                    # Settings & konfigurasi
│   ├── urls.py                        # Root URL routing
│   ├── wsgi.py                        # WSGI entry point
│   └── asgi.py                        # ASGI entry point
│
├── core/                              # Public app (landing, articles, contact)
│   ├── models.py                      # Category, Article, ContactMessage
│   ├── views.py                       # Landing, article list, detail, about, contact
│   ├── urls.py                        # Public URL routes
│   ├── forms.py                       # ContactForm
│   ├── admin.py                       # Admin registration (backup)
│   └── migrations/
│
├── dashboard/                         # Admin panel app
│   ├── views.py                       # Login, CRUD views
│   ├── urls.py                        # Dashboard URL routes
│   ├── forms.py                       # ArticleForm, CategoryForm
│   ├── decorators.py                  # admin_required decorator
│   ├── admin.py
│   └── migrations/
│
├── templates/                         # HTML templates
│   ├── base.html                      # Base layout publik
│   ├── core/
│   │   ├── landing.html               # Landing page
│   │   ├── articles.html              # Article list
│   │   ├── article_detail.html        # Article detail
│   │   ├── about.html                 # About page
│   │   └── contact.html               # Contact form
│   └── dashboard/
│       ├── base.html                  # Dashboard base layout
│       ├── login.html                 # Login page
│       ├── home.html                  # Dashboard overview
│       ├── articles/
│       │   ├── list.html              # Article list (admin)
│       │   ├── form.html              # Article form
│       │   └── delete.html            # Delete confirmation
│       ├── categories/
│       │   ├── list.html              # Category list
│       │   ├── form.html              # Category form
│       │   └── delete.html            # Delete confirmation
│       └── messages/
│           ├── list.html              # Message list
│           ├── detail.html            # Message detail
│           └── delete.html            # Delete confirmation
│
├── static/                            # Static files
│   ├── css/
│   │   ├── style.css                  # Main stylesheet (publik)
│   │   └── dashboard.css              # Dashboard stylesheet
│   └── js/
│       └── main.js                    # Main JavaScript
│
└── media/                             # User uploaded files (auto-created)
    └── articles/                      # Article images
```

## 🔐 Authentication & Security

- **Login**: Username dan password (staff/admin user)
- **Protection**: Semua dashboard view dilindungi dengan `@admin_required` decorator
- **Session**: Django built-in session authentication
- **CSRF**: Django CSRF protection aktif

## 💾 Database Models

### Category
```python
- name: CharField (max 100, unique)
- slug: SlugField (auto-generated)
- icon: CharField (emoji, default: '📁')
- description: TextField
- created_at: DateTimeField (auto_now_add)
```

### Article
```python
- title: CharField (max 255)
- slug: SlugField (auto-generated, unique)
- excerpt: TextField (max 500)
- content: TextField
- image: ImageField (upload_to='articles/%Y/%m/')
- category: ForeignKey(Category)
- status: CharField (draft, published)
- is_featured: BooleanField
- author: CharField (max 100)
- views_count: PositiveIntegerField
- published_at: DateTimeField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### ContactMessage
```python
- name: CharField (max 100)
- email: EmailField
- subject: CharField (max 200)
- message: TextField
- is_read: BooleanField
- created_at: DateTimeField
```

## 🎨 Design & Styling

- **Mobile-first responsive design**
- **CSS Variables untuk theme management**
- **Dark mode support (ready)**
- **Smooth animations dan transitions**
- **Admin dashboard dengan sidebar navigation**

## 🚀 Deployment

### Untuk Production
1. Set `DEBUG = False` di `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Gunakan environment variables untuk `SECRET_KEY`
4. Setup database PostgreSQL/MySQL (optional)
5. Configure static files dengan `python manage.py collectstatic`
6. Deploy ke Heroku, PythonAnywhere, atau server lainnya

## 🐛 Troubleshooting

### Migration Error
```bash
python manage.py makemigrations
python manage.py migrate
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## 📝 Tips & Tricks

### Buat Artikel Featured
Di admin panel, saat membuat/edit artikel, centang "Artikel Unggulan".

### Upload Gambar Artikel
- Format: JPG, PNG, WebP
- Ukuran: Optimal 1200x600px
- Ukuran maksimal: 5MB
- Folder: `/media/articles/`

### Import Data ke Database
```bash
python manage.py shell
# Kemudian manual insert data
```

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Project ini dibuat untuk keperluan pembelajaran. Silakan gunakan dan modifikasi sesuai kebutuhan.

## 👨‍💻 Author

EcoLens — Portal Berita Lingkungan Hidup  
Dibuat dengan ❤️ untuk lingkungan yang lebih baik.

---

## 📚 Dokumentasi Tambahan

### Cara Menambah Artikel
1. Login ke `/admin-panel/`
2. Klik "Tambah Artikel" di menu Artikel
3. Isi form dengan detail artikel
4. Upload gambar (opsional)
5. Pilih status (Draft/Published)
6. Klik "Simpan Artikel"

### Cara Mengelola Kategori
1. Masuk ke dashboard
2. Pilih menu Kategori
3. Klik "Tambah Kategori" untuk kategori baru
4. Gunakan emoji untuk ikon kategori
5. Simpan kategori

### Cara Membaca Pesan Pengunjung
1. Masuk ke dashboard
2. Pilih menu Pesan
3. Klik salah satu pesan untuk melihat detail
4. Pesan otomatis ditandai sebagai "sudah dibaca"
5. Hapus jika tidak perlu lagi

---

**Last Updated**: May 2026  
**Version**: 1.0.0
