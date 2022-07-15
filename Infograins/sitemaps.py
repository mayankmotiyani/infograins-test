from ast import arg
from django.urls import reverse

from Infograins.views import blockchain, services
from .models import *
from django.contrib.sitemaps import Sitemap

class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['services', 'blog','blockchain_service','resources','products']

    def location(self, item):
        return reverse(item)


class Services_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Service.objects.all()

    def location(self, obj) :
        return reverse("services",args=[obj.service_slug])

    def lastmod(self, obj): 
        return obj.service_date

class Product_Sitemap(Sitemap):
    def items(self):
        return Product.objects.all()

    def location(self,obj):
        return reverse("products",args=[obj.product_slug])

    def lastmod(self, obj): 
        return obj.product_date


class Blockchain_Sitemap(Sitemap):
    def items(self):
        return BlockChain.objects.all()

    def location(self,obj):
        return reverse("blockchain_service_data",args=[obj.service_slug])

    def lastmod(self, obj): 
        return obj.service_date


class Resources_Sitemap(Sitemap):
    def items(self):
        return Resource.objects.all()

    def location(self,obj):
        return reverse("resources",args=[obj.resource_slug])

    def lastmod(self, obj): 
        return obj.resource_date



class Blog_Sitemap(Sitemap):
    def items(self):
        return Blog.objects.all()

    def location(self,obj):
        return reverse("blog",args=[obj.blog_slug])

    def lastmod(self, obj): 
        return obj.blog_date



