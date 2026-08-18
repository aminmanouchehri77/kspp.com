from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'core'

# تنظیمات مسیرهای API
router = DefaultRouter()
router.register(r'activities', views.ActivityViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'logos', views.ClientLogoViewSet)
router.register(r'contact', views.ContactMessageViewSet)

urlpatterns = [
    # مسیر صفحه اصلی و صفحات ثابت سایت
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),  # صفحه خدمات اضافه شد
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # مسیر تعویض زبان
    path('switch-language/', views.switch_language, name='switch_language'), # تغییر زبان اضافه شد
    
    # مسیرهای API (پیشوند api/ خواهند داشت)
    path('api/', include(router.urls)),
]
