from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('account/', include('account.urls', namespace='account')),
    path('orders/', include('orders.urls')),
    path('', include('store.urls', namespace='store')),
    path('robots.txt',
         TemplateView.as_view(template_name="robots.txt",
                              content_type="text/plain"),
         ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.page_not_found_view"
