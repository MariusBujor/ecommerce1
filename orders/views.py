import stripe
from cart.cart import Cart
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

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
                user=request.user, full_name=request.POST.get('full_name'), address1=request.POST.get('address1'), country=request.POST.get('country'), city=request.POST.get('city'), post_code=request.POST.get('post_code'), order_key=order_key, total=carttotal)
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

    stripe.api_key = 'sk_test_51LVDiHFR4QsZUb5p0tejkzM9UmMxjVI6bV72sPriGDkzQBEtpRgnzVBrNndY2p5GKunLV3xX1aZWXBMkSbHaMPQH00jVuTaRMY'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret, 'stripe_pkey': settings.PUBLISHABLE_KEY})
