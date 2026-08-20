from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from core.views import switch_language
# 1. مسیرهایی که پیشوند زبان نمی‌گیرند (مانند سیستم تغییر زبان خود جنگو)
urlpatterns = [
    path('i18n/setlang/', switch_language, name='set_language'),  # جایگزین include شد
]

# 2. مسیرهایی که پیشوند زبان می‌گیرند (مثل پنل ادمین و صفحات سایت)
# استفاده از prefix_default_language=False باعث می‌شود زبان پیش‌فرض (فارسی)
# در آدرس سایت پیشوند /fa/ نگیرد و به سئو کمک می‌کند.
urlpatterns += i18n_patterns(
    path('kspphubadmin/', admin.site.urls),
    
    # متصل کردن URL های اپلیکیشن core برای نمایش سایت و API
    path('', include('core.urls')), 
    
    prefix_default_language=False
)

# 3. تنظیمات سرو کردن فایل‌های استاتیک و مدیا در حالت توسعه (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
