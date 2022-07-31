


class Cart():
    """
    A base Cart class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    def add(self, product, qty):

        """
        Adding and updating the users basket session data

        """
        product_id = product.id 

        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'qty': int(qty)}

        # Save the session

        self.session.modified = True

        def __len__(self):
            """ 
            Get the cart data and count the qty of items 
            """
            return sum(item['qty'] for item in self.cart.values())



    