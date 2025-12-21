from .cart import CartManager

def cart(request):
    return {'cart': CartManager(request)}