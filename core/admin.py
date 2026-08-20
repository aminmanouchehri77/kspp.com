from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Activity,
    Product,
    Tag,
    Article,
    ContactMessage,
    ClientLogo,
)


# ==========================================
# تنظیمات عمومی پنل ادمین
# ==========================================
admin.site.site_header = "پنل مدیریت کیان صنعت"
admin.site.site_title = "مدیریت سایت کیان صنعت"
admin.site.index_title = "پیشخوان مدیریت"


# ==========================================
# ۱. مدیریت فعالیت‌ها / حوزه‌های کاری
# ==========================================
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "display_image",
        "icon",
        "order",
    )
    list_editable = ("order",)
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = ("order", "-id")
    list_per_page = 25
    save_on_top = True

    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": (
                "title",
                "slug",
                "image",
                "icon",
                "order",
            ),
        }),
        ("محتوا", {
            "fields": (
                "short_description",
                "content",
            ),
        }),
    )

    @admin.display(description="تصویر")
    def display_image(self, obj):
        if obj.image:
            return format_html(
                """
                <img src="{}"
                     width="55"
                     height="55"
                     style="
                        border-radius: 8px;
                        object-fit: cover;
                        border: 1px solid #ddd;
                     "
                />
                """,
                obj.image.url,
            )
        return "بدون تصویر"


# ==========================================
# ۲. مدیریت محصولات
# ==========================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title_fa",
        "title_en",
        "display_image",
        "display_category",
        "is_featured",
        "order",
        "created_at",
    )
    list_editable = (
        "is_featured",
        "order",
    )
    list_filter = (
        "category",
        "is_featured",
        "created_at",
    )
    search_fields = (
        "title_fa",
        "title_en",
        "description_fa",
        "description_en",
        "slug",
    )
    prepopulated_fields = {
        "slug": ("title_fa",),
    }
    readonly_fields = ("created_at",)
    ordering = ("order", "-created_at")
    list_per_page = 25
    save_on_top = True

    fieldsets = (
        ("اطلاعات پایه", {
            "fields": (
                "category",
                "slug",
                "image",
                "is_featured",
                "order",
                "created_at",
            ),
        }),
        ("محتوای فارسی", {
            "fields": (
                "title_fa",
                "badge_label_fa",
                "description_fa",
            ),
        }),
        ("محتوای انگلیسی", {
            "fields": (
                "title_en",
                "badge_label_en",
                "description_en",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="تصویر")
    def display_image(self, obj):
        if obj.image:
            return format_html(
                """
                <img src="{}"
                     width="55"
                     height="55"
                     style="
                        border-radius: 8px;
                        object-fit: cover;
                        border: 1px solid #ddd;
                     "
                />
                """,
                obj.image.url,
            )
        return "-"

    @admin.display(description="دسته‌بندی", ordering="category")
    def display_category(self, obj):
        return obj.get_category_display()


# ==========================================
# ۳. مدیریت برچسب‌ها
# ==========================================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name_fa",
        "name_en",
        "slug",
    )
    search_fields = (
        "name_fa",
        "name_en",
        "slug",
    )
    prepopulated_fields = {
        "slug": ("name_fa",),
    }
    ordering = ("name_fa",)
    list_per_page = 30
    save_on_top = True

    fieldsets = (
        ("اطلاعات برچسب", {
            "fields": (
                "name_fa",
                "name_en",
                "slug",
            ),
        }),
    )


# ==========================================
# ۴. مدیریت مقالات، اخبار، نمایشگاه‌ها و آکادمی
# ==========================================
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title_fa",
        "display_image",
        "display_category",
        "display_tags",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "category",
        "tags",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title_fa",
        "title_en",
        "content_fa",
        "content_en",
        "slug",
        "tags__name_fa",
        "tags__name_en",
    )
    prepopulated_fields = {
        "slug": ("title_fa",),
    }
    autocomplete_fields = ("tags",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
    list_per_page = 25
    save_on_top = True

    fieldsets = (
        ("اطلاعات پایه", {
            "fields": (
                "category",
                "slug",
                "image",
                "tags",
                "created_at",
                "updated_at",
            ),
        }),
        ("محتوای فارسی", {
            "fields": (
                "title_fa",
                "content_fa",
            ),
        }),
        ("محتوای انگلیسی", {
            "fields": (
                "title_en",
                "content_en",
            ),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="تصویر")
    def display_image(self, obj):
        if obj.image:
            return format_html(
                """
                <img src="{}"
                     width="55"
                     height="55"
                     style="
                        border-radius: 8px;
                        object-fit: cover;
                        border: 1px solid #ddd;
                     "
                />
                """,
                obj.image.url,
            )
        return "-"

    @admin.display(description="دسته‌بندی", ordering="category")
    def display_category(self, obj):
        return obj.get_category_display()

    @admin.display(description="برچسب‌ها")
    def display_tags(self, obj):
        tags = obj.tags.all()

        if not tags:
            return "-"

        return "، ".join(tag.name_fa for tag in tags)


# ==========================================
# ۵. مدیریت پیام‌های فرم تماس
# ==========================================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "is_read",
        "created_at",
    )
    list_filter = (
        "is_read",
        "created_at",
    )
    search_fields = (
        "name",
        "phone",
        "email",
        "message",
    )
    list_editable = ("is_read",)
    readonly_fields = (
        "name",
        "phone",
        "email",
        "message",
        "created_at",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 30
    actions = (
        "mark_as_read",
        "mark_as_unread",
    )

    fieldsets = (
        ("اطلاعات ارسال‌کننده", {
            "fields": (
                "name",
                "phone",
                "email",
            ),
        }),
        ("متن پیام", {
            "fields": ("message",),
        }),
        ("وضعیت پیام", {
            "fields": (
                "is_read",
                "created_at",
            ),
        }),
    )

    @admin.action(description="علامت‌گذاری به‌عنوان بررسی‌شده")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)

        self.message_user(
            request,
            f"{updated} پیام با موفقیت به‌عنوان بررسی‌شده علامت‌گذاری شد.",
        )

    @admin.action(description="علامت‌گذاری به‌عنوان بررسی‌نشده")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)

        self.message_user(
            request,
            f"{updated} پیام به حالت بررسی‌نشده برگشت.",
        )

    def has_add_permission(self, request):
        """
        پیام تماس فقط باید از طریق فرم سایت ثبت شود،
        نه از بخش مدیریت.
        """
        return False


# ==========================================
# ۶. مدیریت لوگوی مشتریان و همکاران
# ==========================================
@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_logo",
        "is_active",
        "order",
    )
    list_editable = (
        "is_active",
        "order",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("order", "-id")
    list_per_page = 30
    save_on_top = True

    fieldsets = (
        ("اطلاعات لوگو", {
            "fields": (
                "name",
                "logo",
                "is_active",
                "order",
            ),
        }),
    )

    @admin.display(description="لوگو")
    def display_logo(self, obj):
        if obj.logo:
            return format_html(
                """
                <img src="{}"
                     width="65"
                     height="55"
                     style="
                        border-radius: 8px;
                        object-fit: contain;
                        background: #ffffff;
                        padding: 4px;
                        border: 1px solid #ddd;
                     "
                />
                """,
                obj.logo.url,
            )
        return "بدون لوگو"
