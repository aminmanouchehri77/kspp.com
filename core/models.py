from django.db import models
from django.utils.translation import get_language


# ==========================================
# ۱. مدل فعالیت‌ها / حوزه‌های کاری
# ==========================================
class Activity(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان فعالیت",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        allow_unicode=True,
        verbose_name="لینک (Slug)",
    )
    short_description = models.TextField(
        verbose_name="توضیح کوتاه",
    )
    content = models.TextField(
        verbose_name="توضیحات کامل",
    )
    image = models.ImageField(
        upload_to="activities/",
        verbose_name="تصویر",
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="کلاس آیکون؛ مثال: bi bi-sun",
        verbose_name="آیکون",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
    )

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "فعالیت"
        verbose_name_plural = "فعالیت‌ها"

    def __str__(self):
        return self.title


# ==========================================
# ۲. مدل محصولات
# ==========================================
class Product(models.Model):
    CATEGORY_CHOICES = (
        ("solar", "تجهیزات خورشیدی"),
        ("smart-home", "هوشمندسازی"),
        ("ai-robotics", "رباتیک و هوش مصنوعی"),
    )

    # ------------------------------
    # محتوای فارسی و انگلیسی محصول
    # ------------------------------
    title_fa = models.CharField(
        max_length=200,
        verbose_name="نام محصول (فارسی)",
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="نام محصول (انگلیسی)",
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        allow_unicode=True,
        verbose_name="لینک (Slug)",
        help_text="یک مقدار یکتا، ترجیحاً انگلیسی؛ مثال: smart-solar-inverter",
    )

    description_fa = models.TextField(
        verbose_name="توضیحات محصول (فارسی)",
    )
    description_en = models.TextField(
        blank=True,
        verbose_name="توضیحات محصول (انگلیسی)",
    )

    image = models.ImageField(
        upload_to="products/",
        verbose_name="تصویر محصول",
    )

    # ------------------------------
    # دسته‌بندی و تنظیمات نمایشی
    # ------------------------------
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="solar",
        verbose_name="دسته‌بندی محصول",
    )

    badge_label_fa = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="نشان محصول (فارسی)",
        help_text="مثال: جدید، پرفروش‌ترین، تخفیف ویژه",
    )
    badge_label_en = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="نشان محصول (انگلیسی)",
        help_text="Example: New, Best Seller, Special Offer",
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="محصول ویژه",
        help_text="برای نمایش محصول در کارت بزرگ‌تر گرید Bento فعال کنید.",
    )

    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
        help_text="عدد کمتر، نمایش زودتر در صفحه محصولات.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت",
    )

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title_fa

    # ------------------------------
    # پراپرتی‌های محلی‌سازی‌شده
    # ------------------------------
    @property
    def title(self):
        language = get_language() or "fa"
        if language.startswith("en") and self.title_en:
            return self.title_en
        return self.title_fa

    @property
    def description(self):
        language = get_language() or "fa"
        if language.startswith("en") and self.description_en:
            return self.description_en
        return self.description_fa

    @property
    def badge_label(self):
        language = get_language() or "fa"
        if language.startswith("en") and self.badge_label_en:
            return self.badge_label_en
        return self.badge_label_fa

    @property
    def category_display(self):
        return self.get_category_display()


# ==========================================
# ۳. مدل مقالات، اخبار، نمایشگاه‌ها و آکادمی
# ==========================================
class Article(models.Model):
    CATEGORY_CHOICES = (
        ("news", "اخبار"),
        ("exhibition", "نمایشگاه‌ها"),
        ("academy", "آکادمی"),
    )

    # ------------------------------
    # محتوای فارسی و انگلیسی مقاله
    # ------------------------------
    title_fa = models.CharField(
        max_length=250,
        verbose_name="عنوان (فارسی)",
    )
    title_en = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="عنوان (انگلیسی)",
    )

    slug = models.SlugField(
        max_length=250,
        unique=True,
        allow_unicode=True,
        verbose_name="لینک (Slug)",
    )

    content_fa = models.TextField(
        verbose_name="محتوا (فارسی)",
    )
    content_en = models.TextField(
        blank=True,
        verbose_name="محتوا (انگلیسی)",
    )

    # ------------------------------
    # دسته‌بندی و تنظیمات نمایشی
    # ------------------------------
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="news",
        verbose_name="دسته‌بندی",
    )
    
    image = models.ImageField(
        upload_to="articles/",
        blank=True,
        null=True,
        verbose_name="تصویر شاخص",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ انتشار",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "مقاله / خبر"
        verbose_name_plural = "مقالات و اخبار"

    def __str__(self):
        return f"{self.title_fa} ({self.get_category_display()})"

    # ------------------------------
    # پراپرتی‌های محلی‌سازی‌شده
    # ------------------------------
    @property
    def title(self):
        """
        عنوان مقاله را طبق زبان فعال سایت برمی‌گرداند.
        """
        language = get_language() or "fa"
        if language.startswith("en") and self.title_en:
            return self.title_en
        return self.title_fa

    @property
    def content(self):
        """
        محتوای مقاله را طبق زبان فعال سایت برمی‌گرداند.
        """
        language = get_language() or "fa"
        if language.startswith("en") and self.content_en:
            return self.content_en
        return self.content_fa

    @property
    def category_display(self):
        """
        نام نمایشی فارسی دسته‌بندی.
        """
        return self.get_category_display()


# ==========================================
# ۴. مدل پیام‌های فرم تماس
# ==========================================
class ContactMessage(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="نام و نام خانوادگی",
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="شماره تماس",
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="ایمیل",
    )
    message = models.TextField(
        verbose_name="متن پیام",
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="خوانده شده / بررسی شده",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        status = "بررسی شده" if self.is_read else "جدید"
        return f"پیام از {self.name} - ({status})"


# ==========================================
# ۵. مدل لوگوی مشتریان و همکاران
# ==========================================
class ClientLogo(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="نام شرکت / همکار",
    )
    logo = models.ImageField(
        upload_to="clients/",
        verbose_name="لوگو",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال برای نمایش",
    )

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "لوگوی همکار"
        verbose_name_plural = "لوگوی"