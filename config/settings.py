"""
Django settings for config project.
Prepared for Kian Sanat (cPanel Deployment Ready)
"""

import os
import environ
from pathlib import Path
from django.utils.translation import gettext_lazy as _  # اضافه شده برای ترجمه نام زبان‌ها

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# ENV Configuration
# ==========================================
env = environ.Env(
    DEBUG=(bool, False)
)
# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# ==========================================
# Security Settings
# ==========================================
SECRET_KEY = env('SECRET_KEY', default='django-insecure-)j6_qo(s2mh3c6en_kcqffxzhkx^3c=@^+a#@_7m#29oac0_j&')
DEBUG = env('DEBUG', default=True)

# تنظیم دامنه‌های مجاز لوکال و سرور به عنوان پیش‌فرض
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    '127.0.0.1',
    'localhost',
    'kspphub.com',
    'www.kspphub.com'
])


# ==========================================
# Application definition
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    
    # اپلیکیشن‌های پروژه
    'accounts',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # <--- مدیریت زبان‌ها (باید بین Session و Common باشد)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # مسیر پوشه قالب‌های اصلی (برای قرار دادن base.html در کنار manage.py)
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # <--- اضافه شده برای دسترسی به زبان در HTML
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==========================================
# Database
# ==========================================
# تنظیم اتصال به دیتابیس MySQL به عنوان پیش‌فرض
DATABASES = {
    'default': env.db(
        'DATABASE_URL', 
        default='mysql://kian_user:Kspp_Local_2026!@127.0.0.1:3306/kian_sanat'
    )
}


# ==========================================
# Password validation
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==========================================
# Internationalization (i18n)
# ==========================================
LANGUAGE_CODE = 'fa' # اصلاح شد: برای تطابق با 'fa' در لیست LANGUAGES
TIME_ZONE = 'Asia/Tehran' # منطقه زمانی ایران
USE_I18N = True
USE_TZ = True

# تعریف زبان‌های پشتیبانی شده در سایت
LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]

# مسیر فایل‌های ترجمه (فایل‌های .po و .mo)
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# ==========================================
# Static and Media Files (cPanel Ready)
# ==========================================
STATIC_URL = '/static/'
# پوشه‌ای که فایل‌های استاتیک در زمان توسعه (لوکال) در آن قرار دارند
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# پوشه‌ای که جنگو تمام فایل‌های استاتیک را برای cPanel آنجا جمع‌آوری می‌کند (دستور collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
# پوشه‌ای که فایل‌های آپلودی کاربران و مدیر سایت در آن ذخیره می‌شوند
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# Custom User Model & Email Config
# ==========================================
AUTH_USER_MODEL = 'accounts.CustomUser'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
