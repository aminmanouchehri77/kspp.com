from django.db import models

# ۱. مدل فعالیت‌ها / حوزه‌های کاری (مثل انرژی خورشیدی، هوش مصنوعی، شهرهای هوشمند و ...)
class Activity(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان فعالیت")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="لینک (Slug)")
    short_description = models.TextField(verbose_name="توضیح کوتاه")
    content = models.TextField(verbose_name="توضیحات کامل")
    image = models.ImageField(upload_to='activities/', verbose_name="تصویر")
    icon = models.CharField(max_length=100, blank=True, help_text="کلاس آیکون (مثلاً از Bootstrap Icons)", verbose_name="آیکون")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "فعالیت"
        verbose_name_plural = "فعالیت‌ها"

    def __str__(self):
        return self.title


# ۲. مدل سخت‌افزارهای هوشمند / محصولات
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name="لینک (Slug)")
    description = models.TextField(verbose_name="توضیحات محصول")
    image = models.ImageField(upload_to='products/', verbose_name="تصویر محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title


# ۳. مدل یکپارچه برای مقالات، اخبار، نمایشگاه‌ها و آکادمی
class Article(models.Model):
    CATEGORY_CHOICES = (
        ('news', 'اخبار'),
        ('exhibition', 'نمایشگاه‌ها'),
        ('academy', 'آکادمی'),
    )
    
    title = models.CharField(max_length=250, verbose_name="عنوان")
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, verbose_name="لینک (Slug)")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='news', verbose_name="دسته‌بندی")
    content = models.TextField(verbose_name="محتوا")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="تصویر شاخص")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مقاله / خبر"
        verbose_name_plural = "مقالات و اخبار"

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


# ۴. مدل فرم تماس با ما (برای پنل ادمین)
class ContactMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تماس")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    message = models.TextField(verbose_name="متن پیام")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده / بررسی شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f"پیام از {self.name} - {'(بررسی شده)' if self.is_read else '(جدید)'}"


# ۵. مدل لوگوی مشتریان و همکاران (اسلایدر صفحه اصلی)
class ClientLogo(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام شرکت / همکار")
    logo = models.ImageField(upload_to='clients/', verbose_name="لوگو")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال برای نمایش")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "لوگوی همکار"
        verbose_name_plural = "لوگوی همکاران"

    def __str__(self):
        return self.name
