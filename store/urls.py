from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    # path('', views.all_products, name='all_products'),
    path('', views.product_all, name='product_all'),
    path('item/<slug:slug>/', views.product_detail, name='product_detail'), 
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

 
]
