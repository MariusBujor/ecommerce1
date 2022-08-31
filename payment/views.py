# import os
import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from cart.cart import Cart
from orders.views import payment_confirmation

# from django.contrib import messages
# from django.http import JsonResponse

# from orders.models import Order

# if os.path.isfile('env.py'):
#      import env

# stripe.api_key = os.environ.get
# ('STRIPE_SECRET_KEY')


def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplace.html')
    

class Error(TemplateView):
    template_name = 'payment/error.html'
    

@login_required
def CartView(request):
    
    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = 'sk_test_51LVDiHFR4QsZUb5p0tejkzM9UmMxjVI6bV72sPriGDkzQBEtpRgnzVBrNndY2p5GKunLV3xX1aZWXBMkSbHaMPQH00jVuTaRMY'
    intent = stripe.PaymentIntent.create(

        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})

    # def checkout_failed(request):
    #     if request.POST.get('action') == 'post':
    #         order_key = request.POST.get
    #         ('order_key')
    #         order = Order.objects.get
    #         (order_key=order_key)
    #         order.delete()
    #         msg = request.POST.get('error')
    #         response = JsonResponse({'msg': msg})
    #         return response


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
