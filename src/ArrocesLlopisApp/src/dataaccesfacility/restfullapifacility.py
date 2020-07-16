import os
import json
import requests
from configurationdialog import Configuration
from datamodel import Customer, Order,Product, Address
import uuid

class DataPersistancesError(Exception):
    """Exception raised for errors in the RestFullAPIFacility.

    Attributes:
        response Code -- input salary which caused the error
        message -- explanation of the error
    """
    CONN_ERROR = 0

    def __init__(self, responseCode,url, body="", server_message =""):
        self.responseCode = responseCode
        self.message = server_message
        self.url = url
        self.body = body
        super().__init__(self.message)

class RestFullAPIFacility:
    # Instance of singleton to be stored
    __instance = None

    @staticmethod
    def getInstance():
        pass
        """ Static access method. """
        if RestFullAPIFacility.__instance is None:
            RestFullAPIFacility()
        return RestFullAPIFacility.__instance

    def __init__(self):
        """ Virtually private constructor. """
        coniguration = self.parseConfigurationFile()

        self.base_url = "http://" + coniguration.host
        self.port = coniguration.port
        self.userName = coniguration.userName
        self.passWord = coniguration.passWord
        self.access_token = None
        self.refresh_token = None

        if RestFullAPIFacility.__instance is not None:
            raise Exception("This class is a singleton! Use getInstance() instead of constructor")
        else:
            # TODO Create class membres
            RestFullAPIFacility.__instance = self

    def isAuthenticated(self):
        if self.access_token != None:
            return True
        else:
            return False

    def refreshToken(self):
        url = self.base_url + ':' + self.port + '/api/token/refresh/'
        data = {
            "refresh": self.refresh_token
        }
        headers = {'Content-type': 'application/json'}
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception as connectionError:
            message = "Exception occurred while performing a POST  operation"
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR,url)
        if response.status_code != 200:
            raise DataPersistancesError(response.status_code,url,json.dumps(data),str(response.content))
        else:
            received_data = json.loads(response.content)
            self.access_token = received_data['access']

    def otainNewToken(self):
        url = self.base_url + ':' + self.port + '/api/token/'
        data = {
            "username": self.userName,
            "password": self.passWord
        }

        headers = {'Content-type': 'application/json'}
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception as connectionError:
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR, url)
        if response.status_code != 200:
            raise DataPersistancesError(response.status_code,url,json.dumps(data),str(response.content))
        else:
            received_data = json.loads(response.content)
            self.access_token = received_data['access']
            self.refresh_token = received_data['refresh']

    @staticmethod
    def parseConfigurationFile():
        filename = 'Configuration.json'
        parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        full_file = parent_path + '/config/' + filename
        with open(full_file) as file:
            data = json.load(file)
            configuration = Configuration()
            configuration.host = data["host"]
            configuration.port = data["port"]
            configuration.userName = data["userName"]
            configuration.passWord = data["passWord"]

            return configuration

    def saveConfigurationToFile(self, configuration):
        filename = 'Configuration.json'
        parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        full_file = parent_path + '/config/' + filename
        data = {}

        data["host"] = configuration.host
        data["port"] = configuration.port
        data["userName"] = configuration.userName
        data["passWord"] = configuration.passWord
        with open(full_file,'w') as outfile:
            json.dump(data, outfile)

    def get_list(self,slug, Element_class, auth):
        url = self.base_url+':'+self.port + slug
        head = None
        if auth:
            head = {'Authorization': 'Bearer {}'.format(self.access_token)}
        try:
            response = requests.get(url, headers=head)
        except Exception as connectionError:
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR,url)

        if response.status_code == 200:
            list_of_elements = []
            received_data = json.loads(response.content)
            next_request = received_data['next']
            results = received_data['results']
            for received_element in results:
                list_of_elements.append(Element_class.fromJSON(received_element))
            if next_request != None:
                #TODO
                raise NotImplementedError
            return list_of_elements
        else:
            raise DataPersistancesError(response.status_code, url,
                                        server_message=str(response.content))

    def get_detail(self, slug,Element_class, elementID, auth):
        url = self.base_url + ':' + self.port + slug+ elementID
        head = None
        if auth:
            head = {'Authorization': 'Bearer {}'.format(self.access_token)}
        try:
            response = requests.get(url, headers=head)
        except Exception as connectionError:
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR,url)
        if response.status_code == 200:
            received_data = json.loads(response.content)
            results = received_data['result']
            return Element_class.fromJSON(results)
        else:
            message = "Error occurred while performing a GET  operation."
            if len(response.content) > 0:
                "Server message: " + str(response.content)
            raise DataPersistancesError(response.status_code, message,url)

    def post_element(self, slug, elemt, auth):
        url = self.base_url + ':' + self.port + slug
        headers = {'Content-type': 'application/json'}
        if auth:
            headers.update({'Authorization': 'Bearer {}'.format(self.access_token)})
        data = elemt.toJson()
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception as connectionError:
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR,url)
        if response.status_code != 201:
            raise DataPersistancesError(response.status_code, url,
                                        json.dumps(data),
                                        str(response.content))

    def update_element(self, slug,elemt, elementID, auth):
        url = self.base_url + ':' + self.port + slug + elementID
        data = elemt.toJson()
        headers = {'Content-type': 'application/json'}
        if auth:
            headers.update({'Authorization': 'Bearer {}'.format(self.access_token)})
        try:
            response = requests.put(url, data=json.dumps(data), headers=headers)
        except Exception as connectionError:
            message = "Exception occurred while performing a PUT  operation"
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR, url)
        if response.status_code != 200:
            raise DataPersistancesError(response.status_code, url,
                                        json.dumps(data),
                                        str(response.content))

    def delete_element(self, slug,elementID, auth):
        url = self.base_url + ':' + self.port + slug + elementID
        head = None
        if auth:
            head = {'Authorization': 'Bearer {}'.format(self.access_token)}
        try:
            response = requests.delete(url,headers=head)
        except Exception as connectionError:
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR,url)
        if response.status_code != 204:
            raise DataPersistancesError(response.status_code, url,
                                        server_message=str(response.content))

    def search_elemet(self, slug,Element_class, searchInfo, auth):
        url = self.base_url + ':' + self.port + slug
        data = searchInfo.toJson()
        if len(data) ==0:
            return []
        headers = {'Content-type': 'application/json'}
        if auth:
            headers.update({'Authorization': 'Bearer {}'.format(self.access_token)})
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception as connectionError:
            message = "Exception occurred while performing a PUT  operation"
            raise DataPersistancesError(DataPersistancesError.CONN_ERROR, url)

        if response.status_code == 200:
            list_of_elements = []
            received_data = json.loads(response.content)
            next_request = received_data['next']
            results = received_data['results']
            for received_element in results:
                list_of_elements.append(Element_class.fromJSON(received_element))
            if next_request != None:
                #TODO
                raise NotImplementedError
            return list_of_elements
        else:
            raise DataPersistancesError(response.status_code, url,
                                        json.dumps(data),
                                        str(response.content))

    def add_customer(self, customer):
        if customer.customerID == "":
            customer.customerID = str(uuid.uuid1())
        self.post_element('/customers/', customer,True)

    def delete_customer(self, customer_id):
        self.delete_element('/customers/', customer_id,True)

    def delete_all_customers(self):
        list_of_allCustomers = self.retrieve_all_customers()
        for customer in list_of_allCustomers:
            self.delete_customer(customer.customerID,True)

    def update_customer(self, customer):
        self.update_element('/customers/',customer, customer.customerID,True)

    def retrieve_customer(self, customer_id):
        return self.get_detail('/customers/', Customer, customer_id,True)

    def retrieve_all_customers(self):
        return self.get_list('/customers/', Customer, True)

    def searchCustomers(self, customerQuery):
        return self.search_elemet('/customers/searches/',Customer,  customerQuery,True)

    def add_order(self, order):
        if order.orderID == "":
            order.orderID = str(uuid.uuid1())
        self.post_element('/orders/', order,True)

    def delete_order(self, orderID):
        self.delete_element('/orders/', orderID,True)

    def delete_all_orders(self):
        list_of_all_orders = self.retrieve_all_orders()
        for order in list_of_all_orders:
            self.delete_order(order.orderID,True)

    def update_order(self, order):
        self.update_element('/orders/',order, order.orderID,True)

    def retrieve_order(self, orderID):
        return self.get_detail('/orders/', Order, orderID,True)

    def retrieve_all_orders(self):
        return self.get_list('/orders/', Order,True)

    def searchOrders(self, orderQuery):
        return self.search_elemet('/orders/searches/', Order,
                                  orderQuery,True)
    def add_product(self, product):
        return self.post_element('/products/', product,True)

    def delete_product(self, product_id):
        self.delete_element('/products/', product_id,True)

    def delete_all_products(self):
        list_of_all_products = self.retrieve_all_products()
        for product in list_of_all_products:
            self.delete_order(product.productID,True)

    def update_product(self, product):
        self.update_element('/products/',product, product.productID ,True)

    def retrieve_product(self, product_id):
        return self.get_detail('/products/', Product, product_id,True)

    def retrieve_all_products(self):
        return self.get_list('/products/', Product,True)
