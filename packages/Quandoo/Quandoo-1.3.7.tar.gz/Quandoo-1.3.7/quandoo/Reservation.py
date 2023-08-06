import json

import requests

from .Error import PoorResponse
from .QuandooModel import urljoin, QuandooModel, QuandooDatetime


class Reservation(QuandooModel):

    def __init__(self, data, agent):
        if type(data) == dict:
            self.id = data["id"]
            self.number = data["number"]
            self.quandooId = data["quandooId"]
            self.status = data["status"]
            self.date = QuandooDatetime.parse_str_qdt(data["startTime"])
            self.startTime = QuandooDatetime.parse_str_qdt(data["startTime"])
            self.endTime = QuandooDatetime.parse_str_qdt(data["endTime"])
            self.capacity = data["capacity"]
            self.merchantId = data["merchantId"]
            self.customerId = data["customerId"]
            self.extraInfo = data["extraInfo"]
            self.createdAt = data["createdAt"]
            self.updatedAt = data["updatedAt"]

        else:
            self.id = data

        self.agent = agent

        super().__init__(data)

    def __str__(self):
        useful_attrs = []
        for key, val in self.__dict__.items():
            if key not in self.useless_attrs:
                if type(val) == QuandooDatetime:
                    if key == "date":
                        val = val.pretty_date().split(", ")[-1]
                    else:
                        val = val.pretty_date().split(", ")[0]
                useful_attrs.append("{}: {}".format(key, val))

        return "{}(\n\t{}\n)".format(
            self.__class__.__name__,
            ",\n\t".join(useful_attrs)
        )

    def _update(self, new_status: str=None, new_capacity: int=None, new_area_id: int=None, new_start_time: QuandooDatetime=None, reservation_tags=[]):
        data = {
            "reservation": {}
        }

        if new_status is not None:
            data["reservation"]["status"] = new_status
        if new_capacity is not None:
            data["reservation"]["capacity"] = new_capacity
        if new_area_id is not None:
            data["reservation"]["areaId"] = new_area_id
        if new_start_time is not None:
            data["reservation"]["dateTime"] = new_start_time.get_qdt()
        if reservation_tags:
            data["reservation"]['reservationTags'] = reservation_tags

        request = f"{self.agent.url}/reservations/{self.id}"
        response = self.agent.make_request("PATCH", request, data=data)
        # response = requests.patch(request, headers=self.agent.headers, json=data)

        # TO DO
        # Change instance variables - by new fetch or local change?
        # new fetch is slower vs local change needs to re calc endTime
        return


    def cancel(self):
        self._update(new_status="CUSTOMER_CANCELED")
        self.status = "CUSTOMER_CANCELED"

    def reconfirm(self):
        self._update(new_status="RECONFIRMED")
        self.status = "RECONFIRMED"

    def change_capacity(self, new_capacity):
        self._update(new_capacity=new_capacity)
        self.capacity = new_capacity


class NewReservation(QuandooModel):

    def __init__(self, data, agent):
        self.id = data["reservation"]["id"]
        self.number = data["reservation"]["number"]
        self.status = data["reservation"]["status"]
        self.customerId = data["customer"]["id"]

        self.agent = agent

        super().__init__(data)

    def get_reservation(self):
        return self.agent.get_reservation(self.id)

