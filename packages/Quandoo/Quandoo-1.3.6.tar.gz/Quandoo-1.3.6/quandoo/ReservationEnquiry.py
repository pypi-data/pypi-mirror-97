import json

import requests

from .Error import PoorResponse
from .QuandooModel import PrettyClass, QuandooModel, QuandooDatetime, urljoin


class ReservationEnquiry(QuandooModel):

    def __init__(self, data, agent):
        self.id = data["id"]
        self.merchantId = data["merchantId"]
        self.customerId = data["customerId"]
        self.capacity = data["capacity"]
        self.startTime = data["startDateTime"]
        self.endTime = data["endDateTime"]
        self.status = data["status"]

        self.agent = agent

        super().__init__(data)

    def __change_status(self, new_status):
        data = {
            "status": new_status
        }
        request = f"{self.agent.url}/reservation-enquiries/{self.id}"
        response = self.agent.make_request('PATCH', data=data)
        # response = requests.patch(request, headers=self.agent.headers, json=data)

        self.status = new_status
        return

    def get_messages(self):
        request = f"{self.agent.url}/reservation-enquiries/{self.id}/messages"
        response = self.agent.make_request("GET", request)
        # response = requests.get(request)

        return [Message(i) for i in json.loads(response.text)["messages"]]


class NewReservationEnquiry(QuandooModel):

    def __init__(self, data, agent):
        self.id = data["reservationEnquiry"]["id"]
        self.customerId = data["customer"]["id"]

        self.agent = agent

        super().__init__(data)

    def get_reservation_enquiry(self):
        return self.agent.get_reservation_enquiry(self.id)


class Message(PrettyClass):

    def __init__(self, data):
        self.senderType = data["senderType"]
        self.message = data["message"]
        self.creationDate = QuandooDatetime.parse_str_qdt(data["creationDate"])
