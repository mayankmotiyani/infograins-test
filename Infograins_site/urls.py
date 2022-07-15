"""Infograins_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from argparse import Namespace
from unicodedata import name
from django.contrib import admin
from django.urls import path, re_path, include
from Infograins.views import *
from . import  settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap


from Infograins.sitemaps import *
# from Infograins.sitemaps import Services_Sitemap
from django.views.generic import TemplateView

sitemaps = {
    'service': Services_Sitemap(),
    'static': Static_Sitemap(),
    'product':Product_Sitemap(),
    'blockchain':Blockchain_Sitemap(),
    'resources' :Resources_Sitemap(),
    'blog' :Blog_Sitemap(),
}
urlpatterns = [
    path('Infograinsadmin/', admin.site.urls),
    path('',company,name='company'),
    # path('',include('Infograins_site.urls')),
    # path('?'.replace('?'," "),company,name='company'),
    # path(r'^$',company),
    # path(' /?'.replace("/?"," "),company,name='company'),
    # path('infograins.com/?'.replace("/?"," ")),
    path('company/',company,name='company'),
    path('services/',services,name='services'),
    path('products/',products,name='products'),
    path('resources/',resources,name='resources'),
    path('blog/',blog,name='blog'),
    path('contact/',contact,name='contact'),
    path('blockchain_services/'.replace("_","-"),blockchain,name='blockchain_service'),
    path('blockchain-services/<slug:s_id>',single_blockchain,name='blockchain_service_data'),
    path('resources/<slug:resource_id>',single_resources,name='resources'),
    path('products/<slug:product_id>',products_single,name='products_slug'),
    path('products/<slug:technology_id>/<slug:product_id>/',products_technologies,name='product_technology'),
    path('blog/<slug:blog_id>',blog_single,name='blog'),
    path('services/<slug:service_id>',services_single,name='services'),
    path('work-flow',workflow,name='work-flow'),    
    path('team/', team, name ='team'),
    path('testimonial/', testimonial, name ='testimonial'),
    path('career/', career, name = 'career'),
    path('help/', help, name = 'help'),
    path('join-event/', join_event, name = "join_event"),
    path('add-event/', add_event, name = "add_event"),
    path('franchise/',franchise_form,name="franchise"),
    path('apply/',Applyjob,name="jobform"),
    path('event/',events, name="event1"), 
    path('privacy-policy/',privacy_policy, name="policy"), 
    path('about-us',aboutus, name="aboutus"),
    path('training', training, name="training"),
    path('site-map',sitemapss, name="sitemapss"),
    # path('event/indiasoft/',events, name="event1"), 
    path('nft/<slug:slug>/', Nft, name='nft'),
    # path('crypto/<slug:slug>', crypto, name='crypto'),
    # path('forks/', firstfork, name='forks'),

    path('forks/<slug:slug>', Fork_data, name='forks'),
    

    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path('robots.txt',TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    path('ckeditor/', include('ckeditor_uploader.urls')),






]
urlpatterns += staticfiles_urlpatterns()
# urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
