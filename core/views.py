from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import TemplateView
from rest_framework import viewsets, mixins
from .models import Activity, Product, Article, ContactMessage, ClientLogo
from .serializers import (
    ActivitySerializer, ProductSerializer, ArticleSerializer,
    ContactMessageSerializer, ClientLogoSerializer
)

# ==========================================
# بخش ویوهای سایت (HTML)
# ==========================================
class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # بعداً می‌توانیم داده‌های دیتابیس را برای رندر مستقیم در HTML به اینجا اضافه کنیم
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ServicesView(TemplateView):
    template_name = 'core/services.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'


# ==========================================
# ویوی تعویض زبان (جایگزین django.conf.urls.i18n.set_language)
# ==========================================
def switch_language(request):
    """
    جایگزین امن‌تر برای ویوی پیش‌فرض set_language جنگو.
    """
    next_url = request.POST.get('next') or request.GET.get('next') or '/'

    # جلوگیری از Open Redirect (حفاظت امنیتی، دقیقاً مثل ویوی اصلی جنگو)
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = '/'

    lang_code = request.POST.get('language')
    valid_codes = dict(settings.LANGUAGES)

    if not lang_code or lang_code not in valid_codes:
        # زبان نامعتبر یا ارسال‌نشده -> فقط برگرد به همان صفحه
        return HttpResponseRedirect(next_url)

    # ۱. حذف هر پیشوند زبانی موجود در ابتدای next_url (اگر وجود دارد)
    path = next_url
    for code, _ in settings.LANGUAGES:
        prefix = f'/{code}/'
        if path.startswith(prefix):
            path = '/' + path[len(prefix):]
            break
        if path == f'/{code}':
            path = '/'
            break

    # ۲. اضافه کردن پیشوند زبان جدید
    default_lang = settings.LANGUAGE_CODE
    if lang_code != default_lang:
        path = f'/{lang_code}' + (path if path != '/' else '/')

    response = HttpResponseRedirect(path)

    cookie_kwargs = {}
    if hasattr(settings, 'LANGUAGE_COOKIE_AGE'):
        cookie_kwargs['max_age'] = settings.LANGUAGE_COOKIE_AGE
    if hasattr(settings, 'LANGUAGE_COOKIE_PATH'):
        cookie_kwargs['path'] = settings.LANGUAGE_COOKIE_PATH
    if hasattr(settings, 'LANGUAGE_COOKIE_DOMAIN'):
        cookie_kwargs['domain'] = settings.LANGUAGE_COOKIE_DOMAIN
    if hasattr(settings, 'LANGUAGE_COOKIE_SECURE'):
        cookie_kwargs['secure'] = settings.LANGUAGE_COOKIE_SECURE
    if hasattr(settings, 'LANGUAGE_COOKIE_HTTPONLY'):
        cookie_kwargs['httponly'] = settings.LANGUAGE_COOKIE_HTTPONLY
    if hasattr(settings, 'LANGUAGE_COOKIE_SAMESITE'):
        cookie_kwargs['samesite'] = settings.LANGUAGE_COOKIE_SAMESITE

    cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
    response.set_cookie(cookie_name, lang_code, **cookie_kwargs)

    translation.activate(lang_code)

    return response


# ==========================================
# بخش ویوهای API (برای PWA و موبایل)
# ==========================================
class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all().order_by('order')
    serializer_class = ActivitySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer

class ClientLogoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClientLogo.objects.all()
    serializer_class = ClientLogoSerializer

class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    کاربران فقط می‌توانند پیام جدید ایجاد کنند (POST)
    و نمی‌توانند پیام‌های دیگران را ببینند یا حذف کنند.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
