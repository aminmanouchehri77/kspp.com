from django.contrib import admin
from django.utils.html import format_html
from .models import Activity, Product, Article, ContactMessage, ClientLogo

# ==========================================
# تنظیمات عمومی پنل ادمین
# ==========================================
admin.site.site_header = "پنل مدیریت کیان صنعت (Orbia AI)"
admin.site.site_title = "مدیریت سایت"
admin.site.index_title = "پیشخوان مدیریت"


# ==========================================
# ۱. مدیریت فعالیت‌ها
# ==========================================
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "display_image", "order")
    list_editable = ("order",)
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "بدون تصویر"
    display_image.short_description = "تصویر"


# ==========================================
# ۲. مدیریت محصولات
# ==========================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title_fa", "display_image", "category", "is_featured", "order", "created_at")
    list_editable = ("is_featured", "order")
    list_filter = ("category", "is_featured", "created_at")
    search_fields = ("title_fa", "title_en", "slug")
    prepopulated_fields = {"slug": ("title_fa",)}
    
    fieldsets = (
        ("اطلاعات پایه", {
            "fields": ("category", "slug", "image", "is_featured", "order"),
        }),
        ("محتوای فارسی", {
            "fields": ("title_fa", "badge_label_fa", "description_fa"),
        }),
        ("محتوای انگلیسی", {
            "fields": ("title_en", "badge_label_en", "description_en"),
            "classes": ("collapse",), # این بخش را به‌صورت پیش‌فرض می‌بندد تا ظاهر پنل خلوت بماند
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "-"
    display_image.short_description = "تصویر"


# ==========================================
# ۳. مدیریت مقالات و اخبار
# ==========================================
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title_fa", "display_image", "category", "created_at", "updated_at")
    list_filter = ("category", "created_at")
    search_fields = ("title_fa", "title_en", "slug")
    prepopulated_fields = {"slug": ("title_fa",)}
    
    fieldsets = (
        ("اطلاعات پایه", {
            "fields": ("category", "slug", "image"),
        }),
        ("محتوای فارسی", {
            "fields": ("title_fa", "content_fa"),
        }),
        ("محتوای انگلیسی", {
            "fields": ("title_en", "content_en"),
            "classes": ("collapse",),
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "-"
    display_image.short_description = "تصویر"


# ==========================================
# ۴. مدیریت پیام‌های تماس
# ==========================================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "phone", "email", "message")
    list_editable = ("is_read",)
    
    # پیام‌های تماس نباید توسط ادمین ویرایش شوند، پس فقط‌خواندنی می‌شوند
    readonly_fields = ("name", "phone", "email", "message", "created_at")
    
    actions = ["mark_as_read", "mark_as_unread"]

    @admin.action(description="علامت‌گذاری به‌عنوان بررسی‌شده")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} پیام به‌عنوان بررسی‌شده علامت‌گذاری شد.")

    @admin.action(description="علامت‌گذاری به‌عنوان بررسی‌نشده")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} پیام به حالت بررسی‌نشده برگشت.")

    # جلوگیری از اضافه کردن پیام جدید توسط ادمین (چون فقط از سایت باید ارسال شود)
    def has_add_permission(self, request):
        return False


# ==========================================
# ۵. مدیریت لوگوی مشتریان
# ==========================================
@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "display_logo", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("name",)
    list_filter = ("is_active",)

    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: contain; background: #fff; padding: 2px;" />', obj.logo.url)
        return "بدون لوگو"
    display_logo.short_description = "لوگو"
