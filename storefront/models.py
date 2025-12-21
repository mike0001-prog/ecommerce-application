from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural= "Categories"
    def __str__(self):
        return  f"{self.name}" 
    
class Product(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to = "product_images/")
    description = models.TextField(max_length=500,default="no description")
    cat = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    sale_price = models.CharField(max_length=100,default=0)
    is_sale = models.BooleanField(default=False)
    def __str__(self):
        return self.name

# class Order(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     time_created=models.DateTimeField(auto_now_add=True)
#     shipping_add = models.TextField(max_length=500)
#     total = models.CharField(max_length=20)
    
#     # def __str__(self):
#     #     return f"#{self.id}" 


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
#     # def __str__(self):
#     #     return f"{self.quantity} X {self.product.name} in cart #{self.order.id}"

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    phone = models.CharField(max_length=11)
    shipping_address = models.TextField(max_length=600)
    amount_paid = models.DecimalField(max_digits=7,decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=100)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"#order {str(self.id)}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=7,decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} X {self.product.name} in cart #{self.order.id}"

class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s wishlist"

class WishListItem(models.Model):
    wishlist  = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return f"#{self.wishlist} wishlist item"