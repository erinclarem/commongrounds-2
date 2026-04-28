from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.core.validators import MinValueValidator


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('merchstore:product_type', args=[str(self.id)])

    class Meta:
        ordering = ['name']
        verbose_name = 'product type'
        verbose_name_plural = 'product types'


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
        )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='products'
    )
    product_image = models.ImageField()
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
        )
    stock = models.PositiveIntegerField()
    status = models.CharField(
        choices=[
            ('available', 'Available'),
            ('on sale', 'On Sale'),
            ('out of stock', 'Out of Stock')
            ],
        default='available',
        )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('merchstore:product_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Transaction(models.Model):
    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transactions' 
        )
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        choices=[
            ('on cart', 'On Cart'),
            ('to pay', 'To Pay'),
            ('to ship', 'To Ship'),
            ('to receive', 'To Receive'),
            ('delivered', 'Delivered')
            ],
    )
    created_on = models.DateTimeField(auto_now_add=True)
