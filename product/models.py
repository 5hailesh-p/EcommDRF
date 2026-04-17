from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=255)
    discription = models.TextField(blank=True)
    category = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} / Q {self.stock}" 