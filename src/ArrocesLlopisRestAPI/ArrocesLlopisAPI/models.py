#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField


import json


class ProductModel(models.Model):

    class Meta:
        db_table = "api_products_table"

    PRODUCT_TYPE = (
        ('Arroz', 'Arroz'),
        ('Otro', 'Otros'),
    )
    PRODUCT_AVALABILITY = (
        ('Disponible', 'Disponible'),
        ('Retirado', 'Retirado'),
        ('Indisponible', 'Indisponible'),
    )

    productID = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    pType = models.CharField( max_length=15, choices=PRODUCT_TYPE)
    price = models.DecimalField(max_digits=4,decimal_places=2, default=0)
    version = models.IntegerField()
    isAvailable = models.CharField( max_length=15, choices=PRODUCT_AVALABILITY)

    @staticmethod
    def listOfFieldNames():
        all_fields = ProductModel._meta.get_fields()
        fieldNames = []
        for field in all_fields:
            fieldNames.append(field.name)
        return fieldNames

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class CustomerModel(models.Model):

    class Meta:
        db_table = "api_customes_table"

    GENDER = (
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Empresa', 'Empresa')
    )
    MKT_CHANNEL = (
        ('Directo', 'Directo'),
        ('RedSocial', 'RedSocial'),
        ('Búsqueda', 'Búsqueda'),
        ('Recomendado', 'Recomendado')
    )
    customerID = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField()
    telNumbers = ArrayField(models.CharField(max_length=50))
    name = models.CharField(max_length=50)
    registrationDate = models.DateField()
    surnames = models.CharField(max_length=50)
    gender = models.CharField(max_length=8, choices=GENDER)
    marketingChannel = models.CharField(max_length=15, choices=MKT_CHANNEL)
    address = JSONField()

    #  A JSON containing an Address
    #
    #   - street
    #   - flat
    #   - city
    #   - province
    #   - postalCode
    #   - country

    def __repr__(self):

        return '{0} {1}'.format(self.name, self.surnames)

    def __str__(self):
        return '{0} {1}'.format(self.name, self.surnames)

    @staticmethod
    def listOfFieldNames():
        all_fields = CustomerModel._meta.get_fields()
        fieldNames = []
        for field in all_fields:
            fieldNames.append(field.name)
        return fieldNames


class Address:
    def __init__(self,street,flat,city, province, postalCode, country):
        self.street = street
        self.flat = flat
        self.city = city
        self.province = province
        self.postalCode = postalCode
        self.country = country

    @staticmethod
    def fromJSONString(jsonStrValue):
        addressJSON = json.loads(jsonStrValue)

        return Address(addressJSON["street"],addressJSON["flat"],
                       addressJSON["city"],addressJSON["province"],
                       addressJSON["postalCode"], addressJSON["country"])

    def __repr__(self):

        return '{0} {1}, {2} {3} {4} {5}'.format(
            self.street, self.flat,self.city,
            self.province, str(self.postalCode),
            self.country)


class OrderModel(models.Model):

    class Meta:
        db_table = "api_orders_table"

    ORDER_STATUS = (
        ('Pendiente', 'Pendiente'),
        ('Cobrada', 'Cobrada'),
        ('Cancelada', 'Cancelada'),
    )
    DELIVERY = (
        ('13:00', '13:00'),
        ('13:30', '13:30'),
        ('14:00', '14:00'),
        ('14:30', '14:30'),
        ('15:00', '15:00'),
        ('15:30', '15:30'),
    )
    orderID = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.PROTECT)
    status = models.CharField( max_length=15, choices=ORDER_STATUS)
    requestDate = models.DateField()
    listOfProducts = models.ManyToManyField(ProductModel)
    amountOfProducts = ArrayField(models.IntegerField())
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    deliveryTime = models.CharField(max_length=5, choices=DELIVERY)

    @staticmethod
    def listOfFieldNames():
        all_fields = OrderModel._meta.get_fields()
        fieldNames = []
        for field in all_fields:
            fieldNames.append(field.name)
        return fieldNames

    def __repr__(self):
        return self.orderID

    def __str__(self):
        return self.orderID


class DeliveryAvailabilityModel(models.Model):
    class Meta:
        db_table = "api_delivery_availability_table"

    date = models.CharField(max_length=100, primary_key=True)
    H_1300 = models.IntegerField(default=0, validators=[
            MaxValueValidator(6),
            MinValueValidator(0)])
    H_1330 = models.IntegerField(default=0, validators=[
            MaxValueValidator(6),
            MinValueValidator(0)])
    H_1400 =models.IntegerField(default=0, validators=[
            MaxValueValidator(6),
            MinValueValidator(0)])
    H_1430 = models.IntegerField(default=0, validators=[
            MaxValueValidator(6),
            MinValueValidator(0)])
    H_1500 = models.IntegerField(default=0, validators=[
            MaxValueValidator(6),
            MinValueValidator(0)])
    H_1530 = models.IntegerField(default=0, validators=[
            MaxValueValidator(6),
            MinValueValidator(0)])
