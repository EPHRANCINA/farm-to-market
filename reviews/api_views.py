from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from products.models import Product

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return Review.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = Product.objects.get(id=product_id)
        
        # Check if user has already reviewed this product
        if Review.objects.filter(product=product, customer=self.request.user).exists():
            raise serializers.ValidationError(
                {"detail": "You have already reviewed this product."}
            )
        
        serializer.save(customer=self.request.user, product=product) 