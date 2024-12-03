from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# State choices
STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),  # Corrected "Asam" to "Assam"
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Daman and Diu', 'Daman and Diu'),
    ('Uttar Pradesh', 'Uttar Pradesh'),  # Corrected "Utter Pradesh" to "Uttar Pradesh"
    ('West Bengal', 'West Bengal')
)

# Customer Model
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return self.name  # Returning name instead of id for better readability


# Category choices
CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear')
)

# Product Model
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='products/')  # Corrected upload path

    def __str__(self):
        return self.title  # Returning title instead of id for better readability


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart {self.id} - User {self.user.username}"


# Status choices
STATUS_CHOICES = (
    ('PENDING', 'PENDING'),
    ('PACKED', 'PACKED'),
    ('ON THE WAY', 'ON THE WAY'),
    ('DELIVERED', 'DELIVERED'),
    ('CANCELED', 'CANCELED')  # Corrected spelling of "CANCELE"
)

# OrderPlaced Model
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Changed to PositiveIntegerField for consistency
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
