# !/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import CustomerModel
from .models import OrderModel
from .models import ProductModel
from .models import DeliveryAvailabilityModel

import re


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ('productID','name', 'pType','price','version','isAvailable')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ('customerID','email','telNumbers','name','surnames',
                  'gender','marketingChannel','registrationDate' ,'address')

    #  Validator at field level
    def validate_telNumbers(self, value):
        """
        Check that the values al string of 9 digits post is about Django.
        """
        for telNumbers in value:
            if self.isTelNumberValid(telNumbers) is False:
                raise serializers.ValidationError(
                    'Telephone['+telNumbers+']number has not valid value')
        return value

    def isTelNumberValid(self,telNumbers):
        telRregex = '(\+34|0034|34)?[ -]*(6|7|9)[ -]*([0-9][ -]*){8}'
        if (re.search(telRregex, telNumbers)):
            return True
        else:
            return False


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ('orderID','customer','status', 'requestDate',
                  'listOfProducts','amountOfProducts','price',
                  'deliveryTime')

    #  Validator at object level
    def validate(self, data):
        """
        Check that serialized order is valid
        """
        products_list_len = len(data['listOfProducts'])
        amount_list_len = len(data['amountOfProducts'])

        if products_list_len != amount_list_len:
            raise serializers.ValidationError(
                "Number of listed products has to be equal to the listed "
                "amount of products")
        else:
            return data

    def __repr__(self):
        return self.orderID

    def __str__(self):
        return self.orderID


class DeliveryAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAvailabilityModel
        fields = ('date', 'H_1300', 'H_1330', 'H_1400', 'H_1430',
                  'H_1500','H_1530')
