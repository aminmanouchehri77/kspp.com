from rest_framework import serializers
from .models import Activity, Product, Article, ContactMessage, ClientLogo

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    # برای اینکه علاوه بر مقدار انگلیسی (news)، نام نمایشی فارسی (اخبار) را هم داشته باشیم
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        # فیلد is_read (خوانده شده) نباید توسط کاربر عادی مقداردهی شود
        read_only_fields = ['is_read'] 


class ClientLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLogo
        fields = '__all__'
