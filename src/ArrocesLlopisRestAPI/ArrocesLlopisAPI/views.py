#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import OrderModel
from .models import ProductModel
from .models import CustomerModel
from .models import DeliveryAvailabilityModel

from rest_framework import status

from rest_framework.decorators import api_view,pretty_name

from rest_framework.response import Response

from django.db.models import Q
from functools import reduce
from operator import and_
from datetime import datetime

from .serializers import CustomerSerializer
from .serializers import OrderSerializer
from .serializers import ProductSerializer
from .serializers import DeliveryAvailabilitySerializer


@api_view(['GET', 'POST'])
def product_list_view(request):

    if request.method == 'GET':
        productsQuerySet = ProductModel.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(productsQuerySet, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({'result': product_serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(request, productID):
    if request.method == 'GET':
        #  Recover object from database
        try:
            productQuerySet  = ProductModel.objects.get(pk=productID)
        except ProductModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        productSerializer = ProductSerializer(productQuerySet)
        return Response({'result': productSerializer.data})

    if request.method == 'PUT':
        try:
            productQuerySet = ProductModel.objects.get(pk=productID)
            productSerializer = ProductSerializer(productQuerySet,
                                                          data=request.data)
            if productSerializer.is_valid():
                productSerializer.save()
                return Response({'result': productSerializer.data})
            return Response(productSerializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        except ProductModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            prodctQuerySet  = ProductModel.objects.get(pk=productID)
        except ProductModel.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        prodctQuerySet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def order_list_view(request):

    if request.method == 'GET':
        ordersQuerySet = OrderModel.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(ordersQuerySet, request)
        order_serializer = OrderSerializer(result_page,many=True)
        return paginator.get_paginated_response(order_serializer.data)

    if request.method == 'POST':
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({'result': order_serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail_view(request, orderID):
    if request.method == 'GET':
        try:
            orderQuerySet  = OrderModel.objects.get(pk=orderID)
        except OrderModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        orderSerializer = OrderSerializer(orderQuerySet)
        return Response({'result': orderSerializer.data})

    if request.method == 'PUT':
        try:
            orderQuerySet = OrderModel.objects.get(pk=orderID)
            orderSerializer = OrderSerializer(orderQuerySet,
                                                          data=request.data)
            if orderSerializer.is_valid():
                orderSerializer.save()
                return Response({'result': orderSerializer.data})
            return Response(orderSerializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except OrderModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            orderQuerySet  = OrderModel.objects.get(pk=orderID)
        except OrderModel.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        orderQuerySet .delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def customer_list_view(request):

    if request.method == 'GET':
        customersQuerySet  = CustomerModel.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(customersQuerySet, request)
        customer_serializer = CustomerSerializer(result_page ,many=True)
        return paginator.get_paginated_response(customer_serializer.data)

    if request.method == 'POST':
        customer_serializer = CustomerSerializer(data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response({'result': customer_serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(customer_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


#  Creamos un metodo para atender ciertas peticiones  y lo decoramos
#  luego lo asignamos a las URLs que correspondan
@api_view(['GET', 'PUT', 'DELETE'])
def customer_details_view(request, customerID):

    if request.method == 'GET':
        #  Recover object from database
        try:
            customerQuerySet  = CustomerModel.objects.get(pk=customerID)
        except CustomerModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        customer_serializer = CustomerSerializer(customerQuerySet)
        return Response({'result': customer_serializer.data})

    if request.method == 'PUT':
        try:
            customerQuerySet = CustomerModel.objects.get(pk=customerID)
            customerSerializer = CustomerSerializer(customerQuerySet,
                                                          data=request.data)
            if customerSerializer.is_valid():
                customerSerializer.save()
                return Response({'result': customerSerializer.data})
            return Response(customerSerializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        except CustomerModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            customerQuerySet  = CustomerModel.objects.get(pk=customerID)
        except CustomerModel.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        customerQuerySet .delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#  Creamos un metodo para las búsquedas  ciertas peticiones  y lo decoramos
#  luego lo asignamos a las URLs que correspondan
# @api_view(['POST'])
# def customer_searches_view_byParams(request):
#     if request.method == 'POST':
#         listOfFieldNames = CustomerModel.listOfFieldNames()
#
#         searchedValues = {}
#         for fieldName in listOfFieldNames:
#             parameterValue = request.query_params.get(fieldName)
#             if parameterValue is not None:
#                 searchedValues.update({fieldName: parameterValue})
#
#         responseDataSerialized = serachCustomers(searchedValues)
#
#         return Response(status=status.HTTP_200_OK,
#                         data=responseDataSerialized.data)

@api_view(['POST'])
def customer_searches_view_byBody(request):
    if request.method == 'POST':
        errorMessage = validateRequest(request,CustomerModel)
        if len(errorMessage) != 0:
                return Response(errorMessage,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            paginator = PageNumberPagination()
            responseDataSerialized = serachCustomers(request, paginator)
            return paginator.get_paginated_response(responseDataSerialized.data)

def serachCustomers(request, paginator):
    parts = []
    search = request.data
    for field in search.keys():
        if field == 'telNumbers':
            parts.append(Q(**{field + '__contains': '{'+search[field]+'}'}))
        elif field == 'address':
            parts.append(Q(**{field + '__contains': search[field]}))
        else:
            parts.append(Q(**{field: search[field]}))
    query = reduce(and_, parts)
    customerQuerySet = CustomerModel.objects.filter(query)
    result_page = paginator.paginate_queryset(customerQuerySet, request)
    return CustomerSerializer(result_page, many=True)


@api_view(['POST'])
def order_searches_view_byBody(request):
    if request.method == 'POST':
        error_message = validateRequest(request,OrderModel)
        if len(error_message) != 0:
                return Response(error_message,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            paginator = PageNumberPagination()
            responseDataSerialized = searchOrder(request, paginator)
            if responseDataSerialized is None:
                return Response(status=status.HTTP_200_OK,
                                data='No result for your search')
            else:
                return paginator.get_paginated_response(responseDataSerialized.data)


def searchOrder(request, paginator):
    parts = []
    search = request.data
    for field in search.keys():
        if field == 'listOfProducts':
            listOfProducts = search[field]
            for product in listOfProducts:
                parts.append(Q(**{field + '__productID': product}))
        elif field == 'amountOfProducts':
            listOfAmountOfProducts = search[field]
            for amount in listOfAmountOfProducts:
                parts.append(
                    Q(**{field + '__contains': '{' + str(amount) + '}'}))
            pass
        else:
            parts.append(Q(**{field: search[field]}))
    if len(parts) > 0:
        query = reduce(and_, parts)
        orderQuerySet = OrderModel.objects.filter(query)
        result_page = paginator.paginate_queryset(orderQuerySet, request)
        return OrderSerializer(result_page, many=True)
    else:
        return None


@api_view(['POST'])
def products_searches_view_byBody(request):
    if request.method == 'POST':
        error_message = validateRequest(request,ProductModel)
        if len(error_message) != 0:
                return Response(error_message,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            paginator = PageNumberPagination()
            responseDataSerialized = searchProduct(request, paginator)
            return paginator.get_paginated_response(responseDataSerialized.data)


def searchProduct(request, paginator):
    parts = []
    search = request.data
    for field in search.keys():
        parts.append(Q(**{field: search[field]}))
    query = reduce(and_, parts)
    productQuerySet = ProductModel.objects.filter(query)
    result_page = paginator.paginate_queryset(productQuerySet, request)
    return ProductSerializer(result_page, many=True)


def validateRequest(request, model):
    error_message = {}
    if isinstance(request.data, list):
        error_message.update(
            {'Error': 'List is not allowed you, '
                      'have to pass search values in a JSON object'})
    else:
        for field in request.data.keys():
            if field not in model.listOfFieldNames():
                error_message.update(
                    {field: 'is not a queryable field for customer'})
    return error_message


@api_view(['GET', 'POST'])
def delivery_availabilities_list_view(request):

    if request.method == 'GET':
        daQuerySet = DeliveryAvailabilityModel.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(daQuerySet, request)
        da_serializer = DeliveryAvailabilitySerializer(result_page, many=True)
        return paginator.get_paginated_response(da_serializer.data)

    if request.method == 'POST':
        da_serializer = DeliveryAvailabilitySerializer(data=request.data)
        if da_serializer.is_valid():
            da_serializer.save()
            return Response({'result': da_serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(da_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

def validateRequestDateFormat(date):
    error_message = None
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        error_message = {'Error': 'Invalid date format. [ ' + date +
                                 ' ] does not matach with  YYYY-MM-DD format'}
    return error_message

@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated,])
def delivery_availabilities_details_view(request, date):

    errorMessage = validateRequestDateFormat(date)
    if errorMessage is not None:
        return Response(errorMessage,
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            daQuerySet = DeliveryAvailabilityModel.objects.get(pk=date)
            da_serializer = DeliveryAvailabilitySerializer(daQuerySet)
            return Response({'result': da_serializer.data}, status=status.HTTP_200_OK)

        except DeliveryAvailabilityModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            daQuerySet = DeliveryAvailabilityModel.objects.get(pk=date)
            daSerializer = DeliveryAvailabilitySerializer(daQuerySet,
                                                          data=request.data)
            if daSerializer.is_valid():
                daSerializer.save()
                return Response({'result': daSerializer.data})
            return Response(daSerializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        except DeliveryAvailabilityModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            daQuerySet  = DeliveryAvailabilityModel.objects.get(pk=date)
        except DeliveryAvailabilityModel.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        daQuerySet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


class PaginationExampleView(generics.ListCreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

