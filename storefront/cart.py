from .models import Product
from authentication.models import Cart, CartItem
from storefront.models import Product
class CartManager():
    def __init__(self, request):
        self.session = request.session
        cart_id = self.session.get('cart_id')
        recently_viewed = self.session.get('recently_viewed')
        if "cart_id" not in request.session:
            cart_id = request.session["cart_id"] = {}
        if "recently_viewed" not in request.session:
            recently_viewed = request.session["recently_viewed"] = {}    
        self.recently_viewed = recently_viewed
        self.cart = cart_id
        self.cached_cart = None
        if request.user.is_authenticated:
            try:
                self.cached_cart = Cart.objects.get(user=request.user)
                # if not self.cart:

                cache = {f"{item.product.id}":item.quantity for item in self.cached_cart.Cart.all()}
                self.cart.update(cache)

                # else:
                #     cart.cart = self.cart
                #     self.cached_cart = cart.cart

                # print(f"cached data {cache}")
                # print(f"data {self.cart}")
            except Exception:
                Cart.objects.create(user=request.user)
    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
	# if that product is in the cart update the amount
        if product_id in self.cart:
            self.cart[product_id] = int(product_qty)
        else:
            # self.cart[product_id] = {"price":str(product.price)}
            self.cart[product_id] = int(product_qty)
            if self.cached_cart is not None:
                product = Product.objects.get(id=product_id)
                
                CartItem.objects.create(cart=self.cached_cart,product=product,quantity=quantity)
           
        self.session.modified = True
        print(self.cached_cart)
    def __len__(self):
        return len(self.cart)
    def get_products(self):
        # get the key of all product in the session
        products_ids = self.cart.keys()
        #use the key to look up products in the database
        products = Product.objects.filter(id__in=products_ids)
        return products
    def get_quants(self):
        quantities = self.cart
        return quantities
    def cart_remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            product= Product.objects.get(id=product_id)
            print("removing item.....")
            if self.cached_cart is not None:
                CartItem.objects.filter(cart=self.cached_cart,product=product).delete()
                print("removed item")
        self.session.modified = True
        print(f"cached {self.cached_cart}")
        print(f"cart {self.cart}")
    def calculate_total(self):
        total = 0
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        quantities = self.cart
        for key,value in quantities.items():
            key= int(key)
            for product in products:
                if key == product.id:
                
                    total = total + (int(product.price) * value)
        return total
    def recentlys_viewed(self,name):
        product = Product.objects.get(name = name)
        self.recently_viewed[product.id] = product.name
        self.session.modified = True

    def return_recently_viewed(self):
        products_ids = self.recently_viewed.keys()
        products = Product.objects.filter(id__in=products_ids)
        return products
    def checkout(self):
        print(self.cart)
        self.cart.clear()
        print(self.cart)
        if self.cached_cart is not None:
                print(self.cached_cart)
                print(self.cached_cart.Cart.all())
                CartItem.objects.filter(cart=self.cached_cart).delete()
                print("removed item")
        self.session.modified = True


       






      