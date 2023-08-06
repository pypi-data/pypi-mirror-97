import locale

from .QuandooModel import QuandooModel


class Customer(QuandooModel):

    def __init__(self, data, agent):
        self.id = data["id"]
        self.firstName = data["firstName"]
        self.lastName = data["lastName"]
        self.email = data["email"]
        self.phoneNumber = data["phoneNumber"]

        super().__init__(data)

    def to_json(self, locale_=None, country=None):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "emailAddress": self.email,
            "phoneNumber": self.phoneNumber,
            "locale": locale_ if locale_ else locale.getdefaultlocale()[0],
            "country": country if country else locale.getdefaultlocale()[0][-2:]
        }
