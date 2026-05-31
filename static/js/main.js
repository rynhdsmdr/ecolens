/* ═══════════════════════════════════════════════════════════════════════
   EcoLens — Main JavaScript
   Mobile menu toggle, smooth scroll, form validation, notifications
   ═══════════════════════════════════════════════════════════════════════ */

// ─────────────────────────────────────────────────────────────────────────
// Utility Functions
// ─────────────────────────────────────────────────────────────────────────

function showNotification(message, type = 'success') {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => alert.remove());
  
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type}`;
  alertDiv.textContent = message;
  alertDiv.style.animation = 'slideIn 0.3s ease-out';
  
  const container = document.querySelector('.container') || document.querySelector('.main-content');
  if (container) {
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
      alertDiv.style.opacity = '0';
      alertDiv.style.transition = 'opacity 0.3s ease-out';
      setTimeout(() => alertDiv.remove(), 300);
    }, 4000);
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Mobile Menu Toggle
// ─────────────────────────────────────────────────────────────────────────

function setupMobileMenu() {
  const menuToggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const navbarMenu = document.querySelector('.navbar-menu');
  
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      if (sidebar) {
        sidebar.classList.toggle('show');
      }
      if (navbarMenu) {
        navbarMenu.classList.toggle('active');
      }
    });
  }
  
  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (sidebar && !sidebar.contains(e.target) && !menuToggle?.contains(e.target)) {
      sidebar.classList.remove('show');
    }
    if (navbarMenu && !navbarMenu.contains(e.target) && !e.target.closest('.navbar')) {
      navbarMenu.classList.remove('active');
    }
  });
}

// ─────────────────────────────────────────────────────────────────────────
// Smooth Scroll
// ─────────────────────────────────────────────────────────────────────────

function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

// ─────────────────────────────────────────────────────────────────────────
// Form Validation
// ─────────────────────────────────────────────────────────────────────────

function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return false;
  
  let isValid = true;
  const fields = form.querySelectorAll('[required]');
  
  fields.forEach(field => {
    const errorElement = field.nextElementSibling;
    
    if (!field.value.trim()) {
      isValid = false;
      if (errorElement && errorElement.classList.contains('form-error')) {
        errorElement.style.display = 'block';
      } else {
        const error = document.createElement('div');
        error.className = 'form-error';
        error.textContent = 'Bidang ini wajib diisi';
        field.parentElement.appendChild(error);
      }
      field.classList.add('is-invalid');
    } else {
      field.classList.remove('is-invalid');
      if (errorElement && errorElement.classList.contains('form-error')) {
        errorElement.style.display = 'none';
      }
    }
    
    // Email validation
    if (field.type === 'email' && field.value.trim()) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(field.value)) {
        isValid = false;
        const error = field.nextElementSibling;
        if (error && error.classList.contains('form-error')) {
          error.textContent = 'Masukkan email yang valid';
        }
        field.classList.add('is-invalid');
      }
    }
  });
  
  return isValid;
}

// ─────────────────────────────────────────────────────────────────────────
// Contact Form Handler
// ─────────────────────────────────────────────────────────────────────────

function setupContactForm() {
  const contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      if (!validateForm('contact-form')) {
        e.preventDefault();
        showNotification('Silakan periksa kembali form Anda', 'error');
      }
    });
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Dashboard Sidebar Active State
// ─────────────────────────────────────────────────────────────────────────

function setupActiveNavigation() {
  const currentUrl = window.location.pathname;
  const navLinks = document.querySelectorAll('.sidebar-link, .navbar-menu a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentUrl.startsWith(href)) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// ─────────────────────────────────────────────────────────────────────────
// Modal Functions
// ─────────────────────────────────────────────────────────────────────────

window.openModal = function(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('show');
  }
};

window.closeModal = function(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('show');
  }
};

// Close modal when clicking outside
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal')) {
    e.target.classList.remove('show');
  }
});

// ─────────────────────────────────────────────────────────────────────────
// Article Search and Filter
// ─────────────────────────────────────────────────────────────────────────

function setupArticleSearch() {
  const searchInput = document.querySelector('.article-search-input');
  const searchForm = document.querySelector('.article-search-form');
  
  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      const query = searchInput?.value.trim();
      if (!query) {
        e.preventDefault();
        showNotification('Masukkan kata kunci pencarian', 'warning');
      }
    });
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Image Preview
// ─────────────────────────────────────────────────────────────────────────

function setupImagePreview() {
  const fileInputs = document.querySelectorAll('input[type="file"]');
  
  fileInputs.forEach(input => {
    input.addEventListener('change', function(e) {
      const file = this.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
          const preview = this.nextElementSibling;
          if (preview && preview.classList.contains('image-preview')) {
            preview.src = event.target.result;
            preview.style.display = 'block';
          }
        };
        reader.readAsDataURL(file);
      }
    });
  });
}

// ─────────────────────────────────────────────────────────────────────────
// Delete Confirmation
// ─────────────────────────────────────────────────────────────────────────

function setupDeleteConfirmation() {
  const deleteButtons = document.querySelectorAll('.btn-delete, .btn-danger[data-confirm]');
  
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      const message = this.getAttribute('data-confirm') || 'Apakah Anda yakin ingin menghapus item ini?';
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });
}

// ─────────────────────────────────────────────────────────────────────────
// Table Row Selection
// ─────────────────────────────────────────────────────────────────────────

function setupTableSelection() {
  const selectAllCheckbox = document.querySelector('.select-all');
  const rowCheckboxes = document.querySelectorAll('.table tbody .row-select');
  
  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener('change', function() {
      rowCheckboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
      });
    });
  }
  
  rowCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      const allChecked = Array.from(rowCheckboxes).every(cb => cb.checked);
      const anyChecked = Array.from(rowCheckboxes).some(cb => cb.checked);
      if (selectAllCheckbox) {
        selectAllCheckbox.checked = allChecked;
        selectAllCheckbox.indeterminate = anyChecked && !allChecked;
      }
    });
  });
}

// ─────────────────────────────────────────────────────────────────────────
// Copy to Clipboard
// ─────────────────────────────────────────────────────────────────────────

window.copyToClipboard = function(text) {
  navigator.clipboard.writeText(text).then(() => {
    showNotification('Teks berhasil disalin', 'success');
  }).catch(() => {
    showNotification('Gagal menyalin teks', 'error');
  });
};

// ─────────────────────────────────────────────────────────────────────────
// Tooltip
// ─────────────────────────────────────────────────────────────────────────

function setupTooltips() {
  document.querySelectorAll('[data-tooltip]').forEach(element => {
    element.addEventListener('mouseenter', function() {
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      tooltip.textContent = this.getAttribute('data-tooltip');
      tooltip.style.cssText = `
        position: absolute;
        background: var(--dark);
        color: white;
        padding: 0.5rem 0.75rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        white-space: nowrap;
        z-index: 1000;
      `;
      document.body.appendChild(tooltip);
      
      const rect = this.getBoundingClientRect();
      tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
      tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
    });
    
    element.addEventListener('mouseleave', function() {
      document.querySelectorAll('.tooltip').forEach(t => t.remove());
    });
  });
}

// ─────────────────────────────────────────────────────────────────────────
// Initialization
// ─────────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
  setupMobileMenu();
  setupSmoothScroll();
  setupContactForm();
  setupActiveNavigation();
  setupArticleSearch();
  setupImagePreview();
  setupDeleteConfirmation();
  setupTableSelection();
  setupTooltips();
  
  console.log('EcoLens JavaScript initialized');
});

// Prevent multiple form submissions
document.addEventListener('DOMContentLoaded', function() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function() {
      const submitButtons = this.querySelectorAll('button[type="submit"]');
      submitButtons.forEach(btn => {
        btn.disabled = true;
        btn.textContent = 'Memproses...';
      });
    });
  });
});
