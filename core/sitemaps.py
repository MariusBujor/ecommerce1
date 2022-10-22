from django.contrib.sitemaps import Sitemap
from store.models import Category, Product


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Category.objects.all()

    def location(self,item):
        return '/search/%s' % (item.slug)


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Product.objects.all()

    def lastmod(self, item):
        return item.updated

    def location(self, item):
        return '/item/%s' % (item.slug)
