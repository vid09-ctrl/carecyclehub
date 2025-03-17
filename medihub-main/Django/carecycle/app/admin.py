from django.contrib import admin
from .models import CUser,Medicine,Order,Payment,Prescription,Cart
# Register your models here.

class CUserAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
        "phone",
        "Customer",
        "address",
        "password",
        "created_at"
        
    ]
class MedicineAdmin(admin.ModelAdmin):
    list_display=[
        "name",
        "description",
        "manufacturer",
        "price",
        "stock_quantity",
        "expiry_date",
        "prescription_required",
        "created_at", 
        "photo"
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "total_price",
        "status",
        "created_at"
    ]
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "userid",
        "productid",
        "qty"
    ] 
   

class PaymentAdmin(admin.ModelAdmin):
    list_display=[
        "order",
        "amount",
        "payment_method",
        "is_successful",
        "timestamp"
    ]
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "image",
        "uploaded_at",
        "approved"
    ]
admin.site.register(CUser, CUserAdmin)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Prescription, PrescriptionAdmin)