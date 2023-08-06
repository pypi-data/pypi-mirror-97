"""
Unofficial library, still in progress

Author:
    Fraser Langton <fraserbasil@gmail.com>


GitHub:
    github.com/fraser-langton/Quandoo

Quandoo API docs:
    docs.quandoo.com
"""

import json
import requests

from .Agent import Agent
from . import config
from .Customer import Customer
from .Error import PoorResponse
from .Merchant import Merchant
from .QuandooModel import urljoin, PrettyClass
from .Reservation import Reservation
from .ReservationEnquiry import ReservationEnquiry


def status():
    request = urljoin(config.base_url, config.version, "status")
    response = requests.get(request)

    return response.status_code


def status_test():
    request = urljoin(config.base_url_test, config.version, "status")
    response = requests.get(request)

    return response.status_code
