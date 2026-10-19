from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import (
    CategoryWithCountSerializer,
    ProductWithReviewsSerializer,
)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer
    lookup_field = 'id'


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    serializer = ProductWithReviewsSerializer(products, many=True)
    return Response(serializer.data)
