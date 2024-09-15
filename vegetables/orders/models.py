from django.db import models
from django.contrib.auth.models import User
from  vendors.models import  Vendor
from product.models import Product
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    def __str__(self):
        return f'{self.user.username} - {self.phone_number}'

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # E.g., 10 for 10% or 10.00 for 10 units off
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)  # Optional usage limit

    def __str__(self):
        return self.code
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Canceled', 'Canceled')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.customer}'

class OrderItem(models.Model):
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order,related_name='items' ,  on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
class Card(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=255)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"Card ending {self.card_number[-4:]} for {self.customer.user.username}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class Promotion(models.Model):
    name = models.CharField(max_length=255, default="Default Name")  # Add a default here
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_active(self):
        from django.utils import timezone
        return self.start_date <= timezone.now() <= self.end_date
    
    def get_discounted_price(self):
        from product.models import Product  # Lazy import here
        return self.product.price * (1 - (self.discount_percentage / 100))
class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=20, choices=[('card', 'Card'), ('paypal', 'Paypal')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)

def complete_payment(order, transaction_id, amount):
    Transaction.objects.create(
        order=order,
        transaction_id=transaction_id,
        payment_method='card',
        amount=amount,
        status='completed'
    )
    order.status = 'completed'
    order.save()
