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


urlpatterns = [
    # ==========================================
    # صفحات HTML سایت
    # ==========================================
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
    path(
        "contact/",
        views.ContactView.as_view(),
        name="contact",
    ),

    # ==========================================
    # تعویض زبان
    # ==========================================
    path(
        "switch-language/",
        views.switch_language,
        name="switch_language",
    ),

    # ==========================================
    # API
    # ==========================================
    path(
        "api/",
        include(router.urls),
    ),
]
