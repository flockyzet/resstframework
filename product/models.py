from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    stars = models.IntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)] 
    ) 

    def __str__(self):
        return f'{self.product.title} - {self.stars} stars'

class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=6)

    def save(self, *args, **kwargs):
        if not self.code:
          
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)