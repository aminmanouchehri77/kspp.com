from rest_framework import serializers
from .models import Activity, Product, Article, ContactMessage, ClientLogo


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    badge_label = serializers.ReadOnlyField()
    category_display = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    content = serializers.ReadOnlyField()
    category_display = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = "__all__"


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["is_read"]


class ClientLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLogo
        fields = "__all__"
