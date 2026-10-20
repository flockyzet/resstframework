import random
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Category, Product, Review, UserConfirmation
from .serializers import (
    CategoryWithCountSerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer
    lookup_field = 'id'


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    serializer = ProductWithReviewsSerializer(products, many=True)
    return Response(serializer.data)


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
        UserConfirmation.objects.create(
            user=user, 
            code=str(random.randint(100000, 999999))
        )
        return user


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('code')
        try:
            user = User.objects.get(username=username)
            confirmation = UserConfirmation.objects.get(user=user)
        except (User.DoesNotExist, UserConfirmation.DoesNotExist):
            raise serializers.ValidationError("неверный пользователь или код.")

        if confirmation.code != code:
            raise serializers.ValidationError("неверный код подтверждения.")

        attrs['user'] = user
        return attrs


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.is_active = True
        user.save()
        user.confirmation.delete()
        return Response({"message": "аккаунт успешно подтвержден"}, status=status.HTTP_200_OK)