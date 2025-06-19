from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'customer', 'customer_name', 
                 'rating', 'comment', 'created_at']
        read_only_fields = ['customer', 'created_at'] 