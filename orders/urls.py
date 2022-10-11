from django.urls import path

from . import views
from .webhook import webhook

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('add/', views.add, name='add'),
    path('thank-you/', views.order_placed, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', webhook, name='webhook'),
]
