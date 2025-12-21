from .models import Order,OrderItem,Product
from .cart import CartManager
def create_order(user,phone,addr,total,mode,request):
            cart = CartManager(request)
            products = cart.get_products()
            quantities = cart.get_quants()
            order = Order.objects.create(user=user,
                                phone=phone,
                                shipping_address=addr,
                                amount_paid=total,
                                mode=mode)
        
            """
            check all the product in the cart(session)
            against the id of the products and create order items
            """
            for product in products:
                for key,value in quantities.items():
                    id = int(key)
                    if id == product.id:
                        p = Product.objects.get(id = product.id)
                        OrderItem.objects.create(order=order,
                                                product=p,
                                                user=user,
                                                quantity = value,
                                                price=product.price)