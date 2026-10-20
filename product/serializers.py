from rest_framework import serializers
from .models import Category, Product, Review
from django.contrib.auth.models import User
from .models import UserConfirmation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'all'

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("название категории должно содержать минимум 2 символа")
        return value


class CategoryWithCountSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("название категории должно содержать минимум 2 символа")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("цена должна быть больше 0")
        return value

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("название товара не может пустовать")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("оценка должна быть впределе от 1 до 5")
        return value


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews']


        class RegisterSerializer(serializers.ModelSerializer):
           class Meta:
            model = User
            fields = ['username', 'password', 'email']
            extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_active=False 
        )
        UserConfirmation.objects.create(user=user)
        return user
