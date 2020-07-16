#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import OrderModel
from .models import ProductModel
from .models import CustomerModel
from .models import DeliveryAvailabilityModel

admin.site.register(CustomerModel)
admin.site.register(ProductModel)
admin.site.register(OrderModel)
admin.site.register(DeliveryAvailabilityModel)