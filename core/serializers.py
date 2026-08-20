from rest_framework import serializers

from .models import (
    Activity,
    Article,
    ClientLogo,
    ContactMessage,
    Product,
    Tag,
)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    سریالایزر محصول با فیلدهای داینامیک وابسته به زبان فعال سایت.
    """

    title = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    badge_label = serializers.ReadOnlyField()
    category_display = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """
    سریالایزر برچسب مقاله.

    فیلد name از پراپرتی مدل Tag خوانده می‌شود و متناسب با
    زبان فعال سایت، نام فارسی یا انگلیسی را بازمی‌گرداند.
    """

    name = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "name_fa",
            "name_en",
            "slug",
        )


class ArticleSerializer(serializers.ModelSerializer):
    """
    سریالایزر مقاله به‌همراه برچسب‌های مرتبط.
    """

    title = serializers.ReadOnlyField()
    content = serializers.ReadOnlyField()
    category_display = serializers.ReadOnlyField()

    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Article
        fields = "__all__"


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = (
            "is_read",
            "created_at",
        )


class ClientLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLogo
        fields = "__all__"
