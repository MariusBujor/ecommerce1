import stripe
from cart.cart import Cart
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Order, OrderItem


def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        carttotal = cart.get_total_price()

        # Check if the order exist
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user=request.user, full_name=request.POST.get('full_name'),
                address1=request.POST.get('address1'),
                country=request.POST.get('country'),
                city=request.POST.get('city'),
                post_code=request.POST.get('post_code'),
                order_key=order_key, total=carttotal)
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(order_id=order_id,
                                         product=item['product'],
                                         price=item['price'])

        response = JsonResponse({'success': 'Return something'})
        return response
    return HttpResponse('hello')


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders


def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplace.html')


class Error(TemplateView):
    template_name = 'payment/error.html'


@login_required
def checkout(request):

    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = settings.SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(
        request, 'payment/home.html', {
            'client_secret': intent.client_secret,
            'stripe_pkey': settings.PUBLISHABLE_KEY}
        )
