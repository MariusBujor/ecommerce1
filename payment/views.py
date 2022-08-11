from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cart.cart import Cart

@login_required
def CartView(request):
    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = 'pk_test_51LVDiHFR4QsZUb5pbOrLsqC1EyFjDyKyjdWCioeB9yu5uD862wCWUwdClDTx2gsH4ReQIZvh6XJniz3O11KXqybW00unW5awdd'
    intent = stripe.PaymentIntent.create(

        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})

