class APIException(Exception):

    def __init__(self, error_type, error_message):
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self):
        return "{} - {}".format(self.error_type, self.error_message)


class QuandooException(APIException):

    def __init__(self, status_code, response, request):
        super().__init__(f'{status_code} {request}', f'{response["errorType"]}: {response["errorMessage"]}')
        self.request = request


class PoorResponse(QuandooException):

    def __init__(self, status_code, response, request):
        super().__init__(status_code, response, request)


class PoorRequest(QuandooException):

    def __init__(self, status_code, response, request):
        super().__init__(status_code, response, request)


class PoorType(APIException):

    def __init__(self, status_code, data):
        super().__init__(status_code, data)
