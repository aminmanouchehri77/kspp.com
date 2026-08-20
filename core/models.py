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
    )
    badge_label_en = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="نشان محصول (انگلیسی)",
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="محصول ویژه",
    )

    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
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
# ۳. مدل برچسب‌های مقالات
# ==========================================
class Tag(models.Model):
    """
    برچسب‌ها برای اتصال به یک یا چند مقاله استفاده می‌شوند.
    مثال:
    هوش مصنوعی، تجهیزات صنعتی، انرژی خورشیدی، نمایشگاه و ...
    """

    name_fa = models.CharField(
        max_length=100,
        verbose_name="نام برچسب (فارسی)",
    )
    name_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام برچسب (انگلیسی)",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        allow_unicode=True,
        verbose_name="لینک برچسب (Slug)",
    )

    class Meta:
        ordering = ["name_fa"]
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"

    def __str__(self):
        return self.name_fa

    @property
    def name(self):
        """
        نام برچسب بر اساس زبان فعال سایت.
        """
        language = get_language() or "fa"

        if language.startswith("en") and self.name_en:
            return self.name_en

        return self.name_fa


# ==========================================
# ۴. مدل مقالات، اخبار، نمایشگاه‌ها و آکادمی
# ==========================================
class Article(models.Model):
    CATEGORY_CHOICES = (
        ("news", "اخبار"),
        ("exhibition", "نمایشگاه‌ها"),
        ("academy", "آکادمی"),
    )

    # عنوان داینامیک دسته‌بندی‌ها برای فارسی و انگلیسی
    CATEGORY_LABELS = {
        "news": {
            "fa": "اخبار",
            "en": "News",
        },
        "exhibition": {
            "fa": "نمایشگاه‌ها",
            "en": "Exhibitions",
        },
        "academy": {
            "fa": "آکادمی",
            "en": "Academy",
        },
    }

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
    # دسته‌بندی و برچسب
    # ------------------------------
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="news",
        verbose_name="دسته‌بندی",
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="articles",
        verbose_name="برچسب‌ها",
        help_text="برچسب‌های مرتبط با این مقاله را انتخاب کنید.",
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

    @property
    def title(self):
        """
        عنوان مقاله مطابق زبان فعال سایت.
        """
        language = get_language() or "fa"

        if language.startswith("en") and self.title_en:
            return self.title_en

        return self.title_fa

    @property
    def content(self):
        """
        محتوای مقاله مطابق زبان فعال سایت.
        """
        language = get_language() or "fa"

        if language.startswith("en") and self.content_en:
            return self.content_en

        return self.content_fa

    @property
    def category_display(self):
        """
        نام دسته‌بندی مطابق زبان فعال سایت.
        """
        language = get_language() or "fa"
        lang_code = "en" if language.startswith("en") else "fa"

        return self.CATEGORY_LABELS.get(
            self.category,
            {},
        ).get(
            lang_code,
            self.get_category_display(),
        )

    @classmethod
    def get_categories_for_language(cls):
        """
        خروجی مناسب برای استفاده در قالب‌ها.

        نمونه:
        [
            {"code": "news", "label": "اخبار"},
            {"code": "exhibition", "label": "نمایشگاه‌ها"},
        ]
        """
        language = get_language() or "fa"
        lang_code = "en" if language.startswith("en") else "fa"

        return [
            {
                "code": code,
                "label": cls.CATEGORY_LABELS.get(
                    code,
                    {},
                ).get(
                    lang_code,
                    default_label,
                ),
            }
            for code, default_label in cls.CATEGORY_CHOICES
        ]


# ==========================================
# ۵. مدل پیام‌های فرم تماس
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
# ۶. مدل لوگوی مشتریان و همکاران
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
        verbose_name_plural = "لوگوهای همکاران"

    def __str__(self):
        return self.name
