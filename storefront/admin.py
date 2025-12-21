from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)

class OrderItemInlines(admin.StackedInline):
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInlines]

admin.site.unregister(Order)
admin.site.register(Order,OrderAdmin)

class WishListItemInlines(admin.StackedInline):
    model = WishListItem
    extra = 0

class WishListAdmin(admin.ModelAdmin):
    model = WishList
    inlines = [WishListItemInlines]

admin.site.register(WishList,WishListAdmin)
admin.site.register(WishListItem)