from django.db import models
from django.conf import settings
from products.models import Product

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_set')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'customer')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.customer.username} for {self.product.name}"
