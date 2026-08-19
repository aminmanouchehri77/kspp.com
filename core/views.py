from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import Q

from rest_framework import mixins, viewsets

from .models import (
    Activity,
    Article,
    ClientLogo,
    ContactMessage,
    Product,
)

from .serializers import (
    ActivitySerializer,
    ArticleSerializer,
    ClientLogoSerializer,
    ContactMessageSerializer,
    ProductSerializer,
)


# ==========================================
# بخش ویوهای صفحات HTML
# ==========================================


class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class ServicesView(TemplateView):
    template_name = "core/services.html"


class ProductsView(TemplateView):
    """
    صفحه نمایش محصولات شرکت کیان صنعت
    """
    template_name = "core/products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all().order_by("order", "-created_at")
        return context


class BlogView(ListView):
    """
    صفحه نمایش لیست مقالات و اخبار (بلاگ)
    """
    model = Article
    template_name = "core/blog.html"
    context_object_name = "articles"
    paginate_by = 4  # تعداد مقالات در هر صفحه

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # ۱. جستجو در متن و عنوان
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title_fa__icontains=q) | 
                Q(title_en__icontains=q) | 
                Q(content_fa__icontains=q) | 
                Q(content_en__icontains=q)
            )
            
        # ۲. فیلتر بر اساس دسته‌بندی
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ارسال جدیدترین مقالات برای سایدبار
        context["recent_posts"] = Article.objects.all().order_by("-created_at")[:3]
        # ارسال لیست دسته‌بندی‌ها برای سایدبار
        context["categories"] = Article.CATEGORY_CHOICES
        # حفظ مقادیر جستجو و فیلتر در URL صفحه‌بندی
        context["current_q"] = self.request.GET.get('q', '')
        context["current_category"] = self.request.GET.get('category', '')
        return context


class BlogDetailView(DetailView):
    """
    صفحه نمایش جزئیات یک مقاله یا خبر
    """
    model = Article
    template_name = "core/blog-details.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class ContactView(TemplateView):
    template_name = "core/contact.html"


# ==========================================
# ویوی تعویض زبان
# ==========================================


def switch_language(request):
    """
    تعویض امن زبان سایت و حفظ مسیر فعلی صفحه
    """

    next_url = request.POST.get("next") or request.GET.get("next") or "/"

    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = "/"

    lang_code = request.POST.get("language") or request.GET.get("language")
    valid_codes = dict(settings.LANGUAGES)

    if not lang_code or lang_code not in valid_codes:
        return HttpResponseRedirect(next_url)

    clean_path = next_url

    for code, _ in settings.LANGUAGES:
        language_prefix = f"/{code}/"

        if clean_path.startswith(language_prefix):
            clean_path = "/" + clean_path[len(language_prefix):]
            break

        if clean_path == f"/{code}":
            clean_path = "/"
            break

    default_language = settings.LANGUAGE_CODE

    if lang_code != default_language:
        if clean_path == "/":
            clean_path = f"/{lang_code}/"
        else:
            clean_path = f"/{lang_code}{clean_path}"

    response = HttpResponseRedirect(clean_path)

    cookie_kwargs = {}

    if hasattr(settings, "LANGUAGE_COOKIE_AGE"):
        cookie_kwargs["max_age"] = settings.LANGUAGE_COOKIE_AGE
    if hasattr(settings, "LANGUAGE_COOKIE_PATH"):
        cookie_kwargs["path"] = settings.LANGUAGE_COOKIE_PATH
    if hasattr(settings, "LANGUAGE_COOKIE_DOMAIN"):
        cookie_kwargs["domain"] = settings.LANGUAGE_COOKIE_DOMAIN
    if hasattr(settings, "LANGUAGE_COOKIE_SECURE"):
        cookie_kwargs["secure"] = settings.LANGUAGE_COOKIE_SECURE
    if hasattr(settings, "LANGUAGE_COOKIE_HTTPONLY"):
        cookie_kwargs["httponly"] = settings.LANGUAGE_COOKIE_HTTPONLY
    if hasattr(settings, "LANGUAGE_COOKIE_SAMESITE"):
        cookie_kwargs["samesite"] = settings.LANGUAGE_COOKIE_SAMESITE

    cookie_name = getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language")

    response.set_cookie(
        cookie_name,
        lang_code,
        **cookie_kwargs,
    )

    translation.activate(lang_code)

    return response


# ==========================================
# بخش ViewSetهای API
# ==========================================


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all().order_by("order")
    serializer_class = ActivitySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("order", "-created_at")
    serializer_class = ProductSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer


class ClientLogoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClientLogo.objects.filter(is_active=True).order_by("order", "-id")
    serializer_class = ClientLogoSerializer


class ContactMessageViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
