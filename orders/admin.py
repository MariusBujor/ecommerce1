from django.contrib import admin

from .models import Order, OrderItem

class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('id', 'created', 'total', 'order_key')

    fields = ('id', 'full_name', 'user', 'address1', 'city', 'country',
              'post_code', 'total', 'order_key')

    list_display = ('id', 'created', 'full_name', 'total')

    ordering = ('-created',)


admin.site.register(Order, OrderAdmin)
