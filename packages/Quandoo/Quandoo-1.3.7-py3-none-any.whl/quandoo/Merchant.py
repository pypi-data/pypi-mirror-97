import json
from datetime import timedelta

import requests

from .Customer import Customer
from .Error import PoorResponse
from .QuandooModel import QuandooModel, QuandooDatetime, urljoin
from .Reservation import Reservation, NewReservation
from .ReservationEnquiry import NewReservationEnquiry


class Merchant(QuandooModel):

    def __init__(self, data, agent):
        if type(data) == dict:
            self.id = data["id"]
            self.name = data["name"]
            address_vals = [i if i in data["location"]["address"].keys() else "" for i in ['number', 'street', 'city', 'country']]
            address_vals[1] = " ".join(address_vals[:1])
            address_vals = address_vals[1:]
            self.address = ", ".join(address_vals)

        else:
            self.id = data

        self.agent = agent

        super().__init__(data)

    def get_customers(self, offset=0, limit=100, modified_since: QuandooDatetime=None, modified_until: QuandooDatetime=None):
        params = {
            "offset": offset,
            "limit": limit
        }
        if modified_since is not None:
            params["modifiedSince"] = modified_since.get_urldt()
        if modified_until is not None:
            params["modifiedUntil"] = modified_until.get_urldt()

        request = f"{self.agent.url}/merchants/{self.id}/customer"
        response = self.agent.make_request("GET", request, params=params)
        # response = requests.get(request, headers=self.agent.headers, params=params)

        return [Customer(i, self.agent) for i in json.loads(response.text)["result"]]

    def get_reservations(self, offset=0, limit=100, earliest=None, latest=None):
        params = {
            "offset": offset,
            "limit": limit
        }
        if earliest is not None:
            params["earliest"] = earliest.get_urldt()
        if latest is not None:
            params["latest"] = latest.get_urldt()

        request = f"{self.agent.url}/merchants/{self.id}/reservations"
        response = self.agent.make_request("GET", request, params=params)
        # response = requests.get(request, headers=self.agent.headers, params=params)

        return [Reservation(i, self.agent) for i in json.loads(response.text)["reservations"]]

    def get_available_times(self, pax: int, qdt: QuandooDatetime, duration=2, area_id=None):
        params = {
            "agentId": self.agent.agent_id,
            "capacity": pax,
            "fromTime": qdt.datetime.strftime("%H:%M"),
            "toTime": (qdt.datetime + timedelta(hours=duration)).strftime("%H:%M")
        }
        if area_id is not None:
            params["areaId"] = area_id

        request = f"{self.agent.url}/merchants/{self.id}/availabilities/{qdt.datetime.strftime('%Y-%m-%d')}/times"
        response = self.agent.make_request("GET", request, params=params)
        # response = requests.get(request, headers=self.agent.headers, params=params)

        return [QuandooDatetime.parse_str_qdt(i["dateTime"]) for i in json.loads(response.text)["timeSlots"]]

    def is_available(self, pax: int, qdt: QuandooDatetime, duration=2, area_id=None):
        return qdt in self.get_available_times(pax, qdt, duration, area_id)

    def get_reviews(self, offset=0, limit=10):
        params = {
            "offset": offset,
            "limit": limit
        }

        request = f"{self.agent.url}/merchants/{self.id}/reviews"
        response = self.agent.make_request("GET", request, params=params)
        # response = requests.get(request, headers=self.agent.headers, params=params)

        return json.dumps(json.loads(response.text), indent=4)

    def create_reservation(self, customer, pax: int, qdt: QuandooDatetime, area_id=None, order_id=None, extra_info=None, reservation_tags=[]):
        data = {
            "reservation": {
                "merchantId": self.id,
                "capacity": pax,
                "dateTime": qdt.get_qdt()
            },
            "customer": customer.to_json(),
            "tracking": {
                "agent": {
                    "id": self.agent.agent_id
                }
            }
        }
        if area_id is not None:
            data["reservation"]["areaId"] = area_id
        if order_id is not None:
            data["reservation"]["orderId"] = order_id
        if extra_info is not None:
            data["reservation"]["extraInfo"] = extra_info
        if reservation_tags:
            data["reservation"]['reservationTags'] = reservation_tags

        request = f"{self.agent.url}/reservations"
        response = self.agent.make_request("PUT", request, data=data)
        # response = requests.put(request, headers=self.agent.headers, json=data)

        return NewReservation(json.loads(response.text), self.agent)

    def create_reservation_enquiry(self, customer, pax: int, start_qdt: QuandooDatetime, end_qdt: QuandooDatetime, message: str):
        data = {
            "reservationEnquiry": {
                "merchantId": self.id,
                "capacity": pax,
                "startDateTime": start_qdt.get_qdt(),
                "endDateTime": end_qdt.get_qdt(),
                "message": message
            },
            "customer": customer.to_json(),
            "tracking": {
                "agent": {
                    "id": self.agent.agent_id
                }
            }
        }

        request = f"{self.agent.url}/reservation-enquiries"
        response = self.agent.make_request("PUT", request, data=data)
        # response = requests.put(request, headers=self.agent.headers, json=data)

        return NewReservationEnquiry(json.loads(response.text), self.agent)

    def get_reservation_tags(self):
        request = f"{self.agent.url}/merchants/{self.id}/reservation_tags"
        response = self.agent.make_request("GET", request)
        # response = requests.put(request, headers=self.agent.headers)

        return json.dumps(json.loads(response.text), indent=4)
