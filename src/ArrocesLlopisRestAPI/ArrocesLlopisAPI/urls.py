#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import views
from django.conf.urls import url

#  Aqui definimos todas las URLS que va a tener nuestra API Rest

# router = routers.DefaultRouter()
# router.register('orders', views.OrderView)
# router.register('customers', views.customer_simple_view)
# router.register('products', views.ProductView)
#
# urlpatterns = [
#     path('', include(router.urls))
# ]

urlpatterns = [
    url(r'^customers/$', views.customer_list_view, name='customers-list'),
    url(r'^customers/searches/$', views.customer_searches_view_byBody, name='customers-searches'),
    url(r'^customers/(?P<customerID>.*)$', views.customer_details_view, name='customers-detail'),


    url(r'^orders/$', views.order_list_view,name='orders-list'),
    url(r'^orders/searches/$', views.order_searches_view_byBody, name='orders-searches'),
    url(r'^orders/(?P<orderID>.*)$', views.order_detail_view, name='order-detail'),

    url(r'^products/$', views.product_list_view),
    url(r'^products/searches/$', views.products_searches_view_byBody),
    url(r'^products/(?P<productID>.*)$', views.product_detail_view),

    url(r'^deliveryAvailabilities/$', views.delivery_availabilities_list_view),
    url(r'^deliveryAvailabilities/(?P<date>.*)$', views.delivery_availabilities_details_view),


    url(r'^productlist/$', views.PaginationExampleView.as_view()),

]