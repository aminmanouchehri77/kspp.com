from django.conf import settings
from django.db.models import (
    Case,
    Count,
    IntegerField,
    Q,
    When,
)
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
)

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
        
        # ارسال ۳ مقاله جدید برای نمایش در بخش وبلاگ صفحه اصلی
        context["latest_articles"] = (
            Article.objects
            .order_by("-created_at")[:3]
        )
        
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class ServicesView(TemplateView):
    template_name = "core/services.html"


class ProductsView(TemplateView):
    """
    صفحه نمایش محصولات شرکت کیان صنعت.
    """

    template_name = "core/products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["products"] = (
            Product.objects
            .all()
            .order_by("order", "-created_at")
        )

        return context


class BlogView(ListView):
    """
    صفحهٔ لیست مقالات و اخبار.

    قابلیت‌ها:
    - نمایش مقاله‌ها با صفحه‌بندی
    - جست‌وجو در عنوان و محتوای فارسی/انگلیسی
    - فیلتر دسته‌بندی
    - فیلتر برچسب
    - ارسال داده‌های لازم برای سایدبار قالب
    """

    model = Article
    template_name = "core/blog.html"
    context_object_name = "articles"
    paginate_by = 4

    def get_queryset(self):
        queryset = (
            Article.objects
            .prefetch_related("tags")
            .order_by("-created_at")
        )

        # ------------------------------
        # جست‌وجو در عنوان و محتوای فارسی/انگلیسی
        # نمونه:
        # /blog/?q=solar
        # ------------------------------
        self.current_q = self.request.GET.get("q", "").strip()

        if self.current_q:
            queryset = queryset.filter(
                Q(title_fa__icontains=self.current_q)
                | Q(title_en__icontains=self.current_q)
                | Q(content_fa__icontains=self.current_q)
                | Q(content_en__icontains=self.current_q)
            )

        # ------------------------------
        # فیلتر دسته‌بندی
        # نمونه:
        # /blog/?category=news
        # ------------------------------
        self.current_category = self.request.GET.get(
            "category",
            "",
        ).strip()

        valid_categories = dict(Article.CATEGORY_CHOICES)

        if (
            self.current_category
            and self.current_category in valid_categories
        ):
            queryset = queryset.filter(
                category=self.current_category
            )
        else:
            # حذف مقدار نامعتبر برای جلوگیری از حفظ آن در Pagination
            self.current_category = ""

        # ------------------------------
        # فیلتر برچسب
        # نمونه:
        # /blog/?tag=artificial-intelligence
        # ------------------------------
        self.current_tag = self.request.GET.get(
            "tag",
            "",
        ).strip()

        if self.current_tag:
            queryset = queryset.filter(
                tags__slug=self.current_tag
            )

        # به‌علت رابطهٔ ManyToMany در تگ‌ها، distinct ضروری است.
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # دریافت مدل Tag از رابطهٔ ManyToMany بدون import مستقیم آن
        tag_model = Article._meta.get_field(
            "tags"
        ).related_model

        # دسته‌بندی‌های داینامیک و چندزبانه.
        # خروجی:
        # [{"code": "news", "label": "اخبار"}, ...]
        context["categories"] = (
            Article.get_categories_for_language()
        )

        # سه مقالهٔ جدید برای سایدبار
        context["recent_posts"] = (
            Article.objects
            .prefetch_related("tags")
            .order_by("-created_at")[:3]
        )

        # همهٔ تگ‌ها برای سایدبار.
        # نکته: name یک @property است؛ پس order_by باید روی name_fa باشد.
        context["all_tags"] = (
            tag_model.objects
            .all()
            .order_by("name_fa")
        )

        # مقادیر فعلی فیلترها برای فرم جست‌وجو، لینک‌ها و Pagination
        context["current_q"] = getattr(
            self,
            "current_q",
            "",
        )

        context["current_category"] = getattr(
            self,
            "current_category",
            "",
        )

        context["current_tag"] = getattr(
            self,
            "current_tag",
            "",
        )

        return context


class BlogDetailView(DetailView):
    """
    صفحهٔ جزئیات مقاله بر اساس slug.

    اولویت نمایش مقالات مرتبط:
    1. بیشترین تعداد برچسب مشترک
    2. دسته‌بندی مشابه
    3. تاریخ انتشار جدیدتر
    """

    model = Article
    template_name = "core/blog-details.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        """
        جلوگیری از Query اضافه هنگام دریافت برچسب‌های مقاله.
        """

        return (
            Article.objects
            .prefetch_related("tags")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        article = self.object

        # دریافت مدل Tag از فیلد ManyToMany
        tag_model = Article._meta.get_field(
            "tags"
        ).related_model

        # چون tags از قبل prefetch شده، این روش Query اضافه ایجاد نمی‌کند.
        article_tags = article.tags.all()

        # شناسه‌های برچسب‌های مقالهٔ فعلی
        article_tag_ids = [
            tag.pk
            for tag in article_tags
        ]

        # دسته‌بندی‌های چندزبانه برای سایدبار
        context["categories"] = (
            Article.get_categories_for_language()
        )

        # تمام برچسب‌ها برای ویجت سایدبار
        # name یک property است؛ بنابراین مرتب‌سازی با name_fa انجام می‌شود.
        context["all_tags"] = (
            tag_model.objects
            .all()
            .order_by("name_fa")
        )

        # برچسب‌های خود مقاله برای بخش Tag Links
        context["article_tags"] = article_tags

        # --------------------------------
        # جدیدترین مقاله‌ها، به‌جز مقالهٔ جاری
        # --------------------------------
        context["recent_posts"] = (
            Article.objects
            .exclude(pk=article.pk)
            .prefetch_related("tags")
            .order_by("-created_at")[:3]
        )

        # --------------------------------
        # مقالات مرتبط
        # --------------------------------
        related_posts = (
            Article.objects
            .exclude(pk=article.pk)
            .prefetch_related("tags")
        )

        if article_tag_ids:
            # مقاله‌های دارای تگ مشترک یا دسته‌بندی یکسان
            related_posts = (
                related_posts
                .filter(
                    Q(tags__in=article_tag_ids)
                    | Q(category=article.category)
                )
                .annotate(
                    shared_tags_count=Count(
                        "tags",
                        filter=Q(tags__in=article_tag_ids),
                        distinct=True,
                    ),
                    same_category_priority=Case(
                        When(
                            category=article.category,
                            then=1,
                        ),
                        default=0,
                        output_field=IntegerField(),
                    ),
                )
                .order_by(
                    "-shared_tags_count",
                    "-same_category_priority",
                    "-created_at",
                )
                .distinct()
            )
        else:
            # اگر مقاله تگی نداشته باشد، فقط مقالات هم‌دسته نمایش داده شوند.
            related_posts = (
                related_posts
                .filter(category=article.category)
                .order_by("-created_at")
            )

        context["related_posts"] = related_posts[:3]

        return context


class ContactView(TemplateView):
    template_name = "core/contact.html"


# ==========================================
# ویوی تعویض زبان
# ==========================================


def switch_language(request):
    """
    تعویض امن زبان سایت و حفظ مسیر فعلی صفحه.
    """

    next_url = (
        request.POST.get("next")
        or request.GET.get("next")
        or "/"
    )

    # جلوگیری از Open Redirect
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = "/"

    lang_code = (
        request.POST.get("language")
        or request.GET.get("language")
    )

    valid_codes = dict(settings.LANGUAGES)

    if not lang_code or lang_code not in valid_codes:
        return HttpResponseRedirect(next_url)

    clean_path = next_url

    # حذف prefix زبان قبلی از URL
    for code, _ in settings.LANGUAGES:
        language_prefix = f"/{code}/"

        if clean_path.startswith(language_prefix):
            clean_path = "/" + clean_path[len(language_prefix):]
            break

        if clean_path == f"/{code}":
            clean_path = "/"
            break

    default_language = settings.LANGUAGE_CODE

    # افزودن prefix زبان مقصد فقط در صورتی که زبان پیش‌فرض نباشد.
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

    cookie_name = getattr(
        settings,
        "LANGUAGE_COOKIE_NAME",
        "django_language",
    )

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
    queryset = (
        Activity.objects
        .all()
        .order_by("order")
    )
    serializer_class = ActivitySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Product.objects
        .all()
        .order_by("order", "-created_at")
    )
    serializer_class = ProductSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API فقط-خواندنی مقاله‌ها به‌همراه برچسب‌ها.
    """

    queryset = (
        Article.objects
        .prefetch_related("tags")
        .order_by("-created_at")
    )
    serializer_class = ArticleSerializer


class ClientLogoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        ClientLogo.objects
        .filter(is_active=True)
        .order_by("order", "-id")
    )
    serializer_class = ClientLogoSerializer


class ContactMessageViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    API ثبت پیام فرم تماس.

    فقط POST مجاز است؛
    لیست، جزئیات، ویرایش و حذف پیام‌ها از طریق API در دسترس نیست.
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
