import datetime


class Customer(object):

    """"""
    def __init__(self, customerID='', email='', telNumbers='', name='',
                 surnames='', address= None, registrationDate=None,
                 marketingChannel='', gender=''):
        """Constructor for Customer"""

        self.customerID = customerID
        self.email = email
        self.telNumbers = telNumbers
        self.name = name
        self.surnames = surnames
        self.gender = gender
        self.marketingChannel = marketingChannel
        self.registrationDate = registrationDate
        self.address = address
        self.registrationDate = registrationDate

    def __repr__(self):
        return self.customerID

    def __str__(self):
        return self.customerID

    def toJson(self):
        data = {}
        if self.customerID != '':
            data['customerID'] = self.customerID
        if self.email != '':
            data['email'] = self.email
        if self.telNumbers != '':
            data['telNumbers'] = self.telNumbers.split(",")
        if self.name != '':
            data['name'] = self.name
        if self.surnames != '':
            data['surnames'] = self.surnames
        if self.gender != '':
            data['gender'] = self.gender
        if self.marketingChannel != '':
            data['marketingChannel'] = self.marketingChannel
        if self.registrationDate != None:
            if type(self.registrationDate) == datetime.datetime:
                data['registrationDate'] = \
                    self.registrationDate.strftime('%Y-%m-%d')
            else:
                data['registrationDate'] = self.registrationDate
        if self.address != None:
            data['address'] = self.address.toJson()
        return data

    @staticmethod
    def fromJSON(json_value):

        customer = Customer()
        customer.customerID = json_value['customerID']
        customer.email = json_value['email']
        customer.telNumbers = listToString(json_value['telNumbers'])
        customer.name = json_value['name']
        customer.surnames = json_value['surnames']
        customer.gender = json_value['gender']
        customer.marketingChannel = json_value['marketingChannel']
        customer.registrationDate = \
            datetime.datetime.strptime(json_value['registrationDate'],
                                       '%Y-%m-%d')
        customer.address = Address.fromJSON(json_value['address'])

        return customer

def listToString(list):
    formated_string = ','.join(map(str, list))
    return formated_string

class Address(object):

    """"""
    def __init__(self, street='', flat='',city='Madrid', province='Madrid',
                 postalCode='', country=''):
        """Constructor for Address"""
        self.street = street
        self.flat = flat
        self.city = city
        self.province = province
        self.postalCode = postalCode
        self.country = country

    def toJson(self):
        data = {}
        if self.street != '':
            data['street'] = self.street
        if self.flat != '':
            data['flat'] = self.flat
        if self.city != '':
            data['city'] = self.city
        if self.street != '':
            data['province'] = self.province
        if self.postalCode != '':
            data['postalCode'] = self.postalCode
        if self.country != '':
            data['country'] = self.country
        return data

    @staticmethod
    def fromJSON(json_value):
        address = Address()

        try:
            address.street = json_value['street']
            address.flat = json_value['flat']
            address.city = json_value['city']
            address.province = json_value['province']
            address.postalCode = json_value['postalCode']
            address.country = json_value['country']
        except KeyError:
            pass
        return address

class Product(object):

    """ """
    def __init__(self, productID='', name='', pType='', price='', version='', isAvailable=''):
        """Constructor for Customer"""
        self.productID = productID
        self.name = name
        self.pType = pType
        self.price = price
        self.version = version
        self.isAvailable = isAvailable

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def toJson(self):
        data = {}
        if self.productID != '':
            data['productID'] = self.productID
        if self.name != '':
            data['name'] = self.name
        if self.pType != '':
            data['pType'] = self.pType
        if self.price != '':
            data['price'] = self.price
        if self.version != '':
            data['version'] = self.version
        if self.isAvailable != '':
            data['isAvailable'] = self.isAvailable
        return data

    @staticmethod
    def fromJSON(json_value):
        product = Product()
        product.productID =json_value['productID']
        product.name = json_value['name']
        product.pType = json_value['pType']
        product.price = json_value['price']
        product.version = json_value['version']
        product.isAvailable = json_value['isAvailable']

        return product

class Order(object):

    """ """
    def __init__(self,orderID='', customer='', status='', requestDate='',
                 listOfProducts='',amountOfProducts='',price='',
                 deliveryTime=''):
        """Constructor for Customer"""
        self.orderID = orderID
        self.customer = customer
        self.status = status
        self.requestDate = requestDate
        self.listOfProducts = listOfProducts
        self.amountOfProducts = amountOfProducts
        self.price = price
        self.deliveryTime = deliveryTime

    def __repr__(self):
        return self.orderID

    def __str__(self):
        return self.orderID

    def toJson(self):
        data = {}
        if self.orderID != '':
            data['orderID'] = self.orderID
        if self.customer != '':
            data['customer'] = self.customer
        if self.status != '':
            data['status'] = self.status
        if self.listOfProducts != '':
            data['listOfProducts'] = self.listOfProducts
        if self.amountOfProducts != '':
            data['amountOfProducts'] = self.amountOfProducts
        if self.price != '':
            data['price'] = self.price
        if self.deliveryTime != '':
            data['deliveryTime'] = self.deliveryTime
        if self.requestDate != None or self.requestDate !='':
            if type(self.requestDate) == datetime.datetime:
                data['requestDate'] = self.requestDate.strftime('%Y-%m-%d')
            else:
                if self.requestDate != '':
                    data['requestDate'] = self.requestDate
        return data

    @staticmethod
    def fromJSON(json_value):
        order = Order()

        order.orderID = json_value['orderID']
        order.customer = json_value['customer']
        order.status = json_value['status']
        order.requestDate = \
            datetime.datetime.strptime(json_value['requestDate'],
                                       '%Y-%m-%d')
        order.listOfProducts = json_value['listOfProducts']
        order.amountOfProducts = json_value['amountOfProducts']
        order.price = json_value['price']
        order.deliveryTime = json_value['deliveryTime']

        return order

class Configuration(object):
    """ """
    def __init__(self, host='', port='', userName='', passWord =''):
        """ Constructor for Configuration """
        self.host = host
        self.port = port
        self.userName = userName
        self.passWord = passWord

