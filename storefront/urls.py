from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
urlpatterns = [ path("home/",home,name="storefront_home"),
                path("product_info/<str:name>/",product_details,name="product_details"),
                path('add/',add, name='cart_add'),
                path('cart/', cart_summary, name='cart_summary'),
                 path("checkout/",checkout,name="storefront_checkout"),
                path('remove/',cart_remove, name='cart_remove'),
                path('billing/',billing, name='storefront_billing'),
                path('orders/',orders, name='storefront_orders'),
                path('like/',like, name='product_like'),
                path('wishlist/',wishlist, name='storefront_wishlist'),
                path('search/',search, name='search_product'),
                path('success/',sucess_page, name='success_page'),
                path('payment/',payment_page, name='payment_page'),
                path('verify/',verify_payment, name='verify'),
                path('failure/',failure_page, name='failure_page'),
                path('category/<str:name>/', category,name="product_cat")
                ]