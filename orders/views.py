from django.shortcuts import render
from django.http.response import JsonResponse

from cart.cart import Cart
from .models import Order, OrderItem



def add(request):
    cart = Cart(request)
    if request.POST.get('auction') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        carttotal = cart.get_total_price()

        # Check if the order exist
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1', total_paid=carttotal, order_key=order_key)
            order_id = order.pk
            for item in the cart:
                
            OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'])
            response = JsonResponse({'success':'Return something'})
        return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)








