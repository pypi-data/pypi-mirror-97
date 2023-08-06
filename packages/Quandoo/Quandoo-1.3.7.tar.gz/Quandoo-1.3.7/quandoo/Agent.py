import json

import requests

from . import config
from .QuandooModel import PrettyClass
from .Merchant import Merchant
from .Error import PoorResponse, APIException
from .Customer import Customer
from .Reservation import Reservation
from .ReservationEnquiry import ReservationEnquiry


class Agent(PrettyClass):
    headers = {
        "accept": "application/json",
        "X-Quandoo-AuthToken": None
    }

    def __init__(self, oauth_token=None, agent_id=None, test=False, url=None):
        self.oauth_token = oauth_token
        self.agent_id = agent_id

        self.url = url if url else f'{config.base_url_test if test else config.base_url}/{config.version}'

        self.headers["X-Quandoo-AuthToken"] = oauth_token

    def make_request(self, method, url, params=None, data=None):
        response = requests.request(
            method=method, url=url, headers=self.headers, params=params, json=data
        )

        if 200 <= response.status_code < 300:
            return response

        if response.status_code == 404:
            res_text = {'errorType': 'ERROR', 'errorMessage': 'Not found'}
        else:
            res_text = json.loads(response.text)

        raise PoorResponse(response.status_code, res_text, url)

    def get_merchant(self, merchant_id):
        request = f"{self.url}/merchants/{merchant_id}"
        response = self.make_request("GET", request)
        # response = requests.get(request, headers=self.headers)

        return Merchant(json.loads(response.text), self)

    def get_customer(self, customer_id):
        request = f"{self.url}/customers/{customer_id}"
        response = self.make_request("GET", request)
        # response = requests.get(request, headers=self.headers)

        return Customer(json.loads(response.text), self)

    def get_reservation(self, reservation_id):
        request = f"{self.url}/reservations/{reservation_id}"
        response = self.make_request("GET", request)
        # response = requests.get(request, headers=self.headers)

        return Reservation(json.loads(response.text), self)

    def get_reservation_enquiry(self, reservation_enquiry_id):
        request = f"{self.url}/reservation-enquiries/{reservation_enquiry_id}"
        response = self.make_request("GET", request)
        # response = requests.get(request, headers=self.headers)

        return ReservationEnquiry(json.loads(response.text), self)

    def merchants(self, params=None):
        request = f"{self.url}/merchants"
        response = self.make_request("GET", request)
        # response = requests.get(request, headers=self.headers, params=params)

        return [Merchant(i, self) for i in json.loads(response.text)['merchants']]
