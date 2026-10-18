from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import (
    CategoryWithCountSerializer,
    ProductWithReviewsSerializer,
)


@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = CategoryWithCountSerializer(categories, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data)
