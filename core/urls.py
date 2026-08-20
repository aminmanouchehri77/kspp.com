from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = "core"


# ==========================================
# مسیرهای API
# ==========================================
router = DefaultRouter()

router.register(
    r"activities",
    views.ActivityViewSet,
    basename="activity",
)

router.register(
    r"products",
    views.ProductViewSet,
    basename="product",
)

router.register(
    r"articles",
    views.ArticleViewSet,
    basename="article",
)

router.register(
    r"logos",
    views.ClientLogoViewSet,
    basename="logo",
)

router.register(
    r"contact",
    views.ContactMessageViewSet,
    basename="contact-message",
)


# ==========================================
# مسیرهای صفحات HTML و API
# ==========================================
urlpatterns = [
    # ------------------------------------------
    # صفحات اصلی سایت
    # ------------------------------------------
    path(
        "",
        views.HomeView.as_view(),
        name="home",
    ),
    path(
        "about/",
        views.AboutView.as_view(),
        name="about",
    ),
    path(
        "services/",
        views.ServicesView.as_view(),
        name="services",
    ),
    path(
        "products/",
        views.ProductsView.as_view(),
        name="products",
    ),

    # ------------------------------------------
    # وبلاگ
    # ------------------------------------------
    path(
        "blog/",
        views.BlogView.as_view(),
        name="blog",
    ),
    path(
        "blog/<slug:slug>/",
        views.BlogDetailView.as_view(),
        name="blog-detail",
    ),

    # ------------------------------------------
    # تماس با ما
    # ------------------------------------------
    path(
        "contact/",
        views.ContactView.as_view(),
        name="contact",
    ),

    # ------------------------------------------
    # تعویض زبان
    # ------------------------------------------
    path(
        "switch-language/",
        views.switch_language,
        name="switch_language",
    ),

    # ------------------------------------------
    # API
    #
    # نمونه آدرس‌ها:
    # /api/activities/
    # /api/products/
    # /api/articles/
    # /api/logos/
    # /api/contact/
    # ------------------------------------------
    path(
        "api/",
        include(router.urls),
    ),
]
