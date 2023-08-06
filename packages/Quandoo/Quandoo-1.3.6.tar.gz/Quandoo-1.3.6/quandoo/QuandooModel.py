import json
import sys
from datetime import datetime
import tzlocal


class PrettyClass:
    useless_attrs = ["api_response", "agent"]

    def __str__(self):
        useful_attrs = ["{}: {}".format(key, val) for key, val in self.__dict__.items() if
                        key not in self.useless_attrs]

        return "{}(\n\t{}\n)".format(
            self.__class__.__name__,
            ",\n\t".join(useful_attrs)
        )

    def __repr__(self):
        return "\n" + indent(str(self))

    def to_tuple(self):
        return tuple([val for key, val in self.__dict__.items() if key not in self.useless_attrs])


class QuandooModel(PrettyClass):

    def __init__(self, data):
        self.api_response = data

    def get_api_response(self):
        return json.dumps(self.api_response, indent=2)


class QuandooDatetime(PrettyClass):
    TIME_RESOLUTION = 15  # minutes

    def __init__(self, *args, **kwargs):
        if type(args[0]) == datetime and len(args) == 1:
            self.datetime = args[0]
        else:
            self.datetime = datetime(*args, **kwargs)

        if not self.datetime.tzinfo:
            self.datetime = tzlocal.get_localzone().localize(self.datetime)

        self.__resolve_time()

    def __str__(self):
        useful_attrs = ["{}: {}".format(key, val) for key, val in self.__dict__.items() if
                        key not in self.useless_attrs] + ["{}: {}".format("q_datetime", self.get_qdt()),
                                                          "{}: {}".format("pretty_date", self.pretty_date())]

        return "{}(\n\t{}\n)".format(
            self.__class__.__name__,
            ",\n\t".join(useful_attrs)
        )

    def __eq__(self, other):
        return self.datetime == other.datetime

    def __lt__(self, other):
        return self.datetime > other.datetime

    @staticmethod
    def now():
        return QuandooDatetime(datetime.now())

    @staticmethod
    def parse_str_qdt(string):
        d = string.split("+")
        d[1] = d[1].replace(":", "")
        return QuandooDatetime(datetime.strptime("+".join(d), "%Y-%m-%dT%H:%M:%S%z"))

    @staticmethod
    def parse_pretty_qdt(string):
        return QuandooDatetime(datetime.strptime(string, "%I:%M %p, %a %d %B %Y"))

    def __resolve_time(self):
        minute = (self.datetime.minute // QuandooDatetime.TIME_RESOLUTION) * QuandooDatetime.TIME_RESOLUTION
        second = microsecond = 0

        self.datetime = self.datetime.replace(minute=minute, second=second, microsecond=microsecond)

    def get_qdt(self):
        return self.datetime.__str__().replace(' ', 'T')

    def get_urldt(self):
        return self.datetime.strftime("%Y-%m-%d %H:%M:%S")

    def pretty_date(self):
        if sys.platform.startswith("win"):
            token = "#"
        elif sys.platform.startswith("linux"):
            token = "-"
        else:
            token = ""
        return self.datetime.strftime("%{token}I:%M %p, %a %{token}d %B %Y".format(**{"token": token}))


def urljoin(*argv):
    return "/".join([str(arg) for arg in argv])


def indent(string, indent_amount=1):
    return "\n".join(["\t" * indent_amount + line for line in string.split("\n")])
