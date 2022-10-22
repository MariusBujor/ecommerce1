from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from .sitemaps import CategorySitemap, ProductSitemap


sitemaps = {
    'category': CategorySitemap,
    'product': ProductSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('account/', include('account.urls', namespace='account')),
    path('orders/', include('orders.urls')),
    path('', include('store.urls', namespace='store')),
    re_path(r'^.*$', TemplateView.as_view(template_name="errors/404.html",
                                          content_type="text/html"),
            ),
    path('robots.txt',
         TemplateView.as_view(template_name="robots.txt",
                              content_type="text/plain"),
         ),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
