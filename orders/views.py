from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse

from cart.cart import Cart
from .models import Order, OrderItem


def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # print('MADE IT HERE')

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        carttotal = cart.get_total_price()

        # Check if the order exist
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
        
                user=request.user, full_name=request.POST.get('full_name'), address1=request.POST.get('custAdd'), order_key=order_key)
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'])

        response = JsonResponse({'success': 'Return something'})
        return response
    return HttpResponse('hello')


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

    # order = Order.objects.get(order_key=data)
    # order_items = OrderItem.objects.filter(order=order)
    # order_items_url = [item.product.mp3.url for item in order_items]
    # subject = 'Your Audio book' 
    # from_email = settings.EMAIL_HOST_USER
    # to = order.email
    # text_message = f'''
    #     Hi there... Yor payment with Audio Bebe Book was succesful.
    #     Here is your books,{"".join(order_items_url)}'''
    # html_message = get_template(("email.html")).render({
    #     'order': order,
    #     'order_items': order_items
    # })
    # message = EmailMultiAlternatives(subject, text_message, from_email, [to])
    # message.attach_alternative(html_message, "text/html")
    # message.send()


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
