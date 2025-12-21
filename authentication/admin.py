from django.contrib import admin
from .models import CustomerProfile,ShippingInfo,AnonymousUserShippingInfo,Cart,CartItem
admin.site.register(CustomerProfile)
admin.site.register(ShippingInfo)
admin.site.register(AnonymousUserShippingInfo)
admin.site.register(Cart)
admin.site.register(CartItem)
class CartItemInline(admin.StackedInline):
    model = CartItem

class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [CartItemInline]
# Register your models here.
admin.site.unregister(Cart)
admin.site.register(Cart,CartAdmin)
