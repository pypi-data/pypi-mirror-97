import json
import os
import requests
import logging

log = logging.getLogger(__name__)


class SomOfficeUserCreationError(Exception):
    def __init__(self, ref, msg):
        message = """
        Error creating the SomOffice user of Partner Ref {}.
        Error message: {}
        """.format(ref, msg)
        super(SomOfficeUserCreationError, self).__init__(message)


class SomOfficeUser:
    endpoint = 'api/admin/import_user/'

    def __init__(self, ref, email, vat, lang):
        self.ref = ref
        self.email = email
        self.vat = vat
        self.lang = lang

    def create(self):
        data = {
            "customerCode": self.ref,
            "customerEmail": self.email,
            "customerUsername": self.vat,
            "customerLocale": self._customerLocale(),
            "resetPassword": bool(os.getenv('SOMOFFICE_RESET_PASSWORD') == 'true')
        }

        try:
            SomOfficeClient().send_request(self.endpoint, data=data)
        except Exception as error:
            log.error("""
            Error creating the SomOffice user. Error Message: {}.
            Data: {}
            """.format(str(error), data))
            raise error

    def _customerLocale(self):
        return {
            "es_ES": "es",
            "ca_ES": "ca",
        }[self.lang]


class SomOfficeClient:
    def __init__(self):
        self.base_url = os.getenv('SOMOFFICE_URL')
        self.user = os.getenv('SOMOFFICE_USER')
        self.password = os.getenv('SOMOFFICE_PASSWORD')

    def send_request(self, endpoint, data):
        """ We only need to send post requests. """
        requests.post(
            "{}{}".format(self.base_url, endpoint),
            auth=(self.user, self.password),
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'},
        )
