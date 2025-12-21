from django.db import models
from django.contrib.auth.models import User
from storefront.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="Cart")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product} x {self.quantity}"
class CustomerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    user_image = models.ImageField(upload_to="profile_pictures/", default="default.jpg")
    user_address = models.TextField(max_length=600,default="not yet updated")
    def __str__(self):
        return f"{self.user} profile"
class ShippingInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True) 
    recipient_phone = models.CharField(max_length=11,default=" ")
    lg_area = models.CharField(max_length=100,default=" ")
    recipient_address = models.TextField(max_length=600,default=" ")
    recipient_name = models.CharField(max_length=100,default=" ")
    
    def __str__(self):
        return f"{self.user} shipping information"
    class Meta:
        verbose_name_plural = "Shipping Informations"
class AnonymousUserShippingInfo(models.Model):
    recipient_phone = models.CharField(max_length=11,default=" ")
    lg_area = models.CharField(max_length=100,default=" ")
    recipient_address = models.TextField(max_length=600,default=" ")
    recipient_name = models.CharField(max_length=100,default=" ")

    def __str__(self):
        return f"{self.recipient_name} shipping information"
    class Meta:
        verbose_name_plural= "Anonymous Users Informations"

# verbose_name_plural
