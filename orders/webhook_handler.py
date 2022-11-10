from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order
from account.models import UserBase


class StripeWH_Handler:
    """Handle Stripe webhooks."""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """ Send the user a confirmation email """
        cust_email = order.user.email
        subject = render_to_string(
            'payment/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'payment/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """
        print(f'Unhandled webhook received: {event["type"]}')
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """ Handle the payment_intent.succeeded webhook event from Stripe """
        intent = event.data.object
        pid = intent.id

        billing_details = intent.charges.data[0].billing_details
        userid = intent.metadata.userid
        grand_total = round(intent.charges.data[0].amount/100, 2)

        user = UserBase.objects.get(id=userid)

        try:
            order = Order.objects.get(order_key__startswith=pid)
            order.billing_status = True
            order.save()

            self._send_confirmation_email(order)

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified \
                        order already in database',
                status=200
            )
        except Order.DoesNotExist:
            order = None
            order = Order.objects.create(
                full_name=billing_details.name,
                user=user,
                country=billing_details.address.country,
                post_code=billing_details.address.postal_code,
                city=billing_details.address.city,
                address1=billing_details.address.line1,
                order_key=pid,
                total=grand_total,
                billing_status=True
                )

            self._send_confirmation_email(order)

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Created \
                    order in webhook',
                status=201
            )
        except Exception as err:
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR : {err}',
                status=500
            )

    def handle_payment_intent_payment_failed(self, event):
        """ Handle the payment_intent.payment_failed
        webhook event from Stripe """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
