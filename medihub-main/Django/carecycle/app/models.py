from django.db import models

# Create your models here


class CUser(models.Model): 
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    USER_TYPES = [('customer', 'Customer'),('admin', 'Admin'),('pharmacist', 'Pharmacist')]
    Customer = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Medicine(models.Model):
    userid = models.ForeignKey(CUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    medicineid = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    expiry_date = models.DateField()
    prescription_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    photo=models.ImageField(upload_to="images", default=None,null=True)

class Cart(models.Model):
    userid = models.ForeignKey(CUser, on_delete=models.SET_NULL, null=True)
    productid = models.ForeignKey(Medicine, to_field="medicineid", on_delete=models.CASCADE, null=True)  
    qty = models.PositiveIntegerField(default=0)



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    is_successful = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Prescription(models.Model):
    user = models.ForeignKey(CUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prescriptions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class Address(models.Model):
    userid = models.ForeignKey("app.CUser", on_delete=models.SET_NULL, null=True, related_name="user_addresses")  
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
