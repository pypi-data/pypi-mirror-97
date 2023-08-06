import os
import json
from mock import patch

from ..sc_test_case import SCTestCase
from ...somoffice.user import SomOfficeUser


@patch.dict(os.environ, {
    'SOMOFFICE_URL': 'https://somoffice.coopdevs.org/',
    'SOMOFFICE_USER': 'user',
    'SOMOFFICE_PASSWORD': 'password'
})
class SomOfficeUserTestCase(SCTestCase):

    @patch('odoo.addons.somconnexio.somoffice.user.requests', spec=['post'])
    def test_create(self, mock_requests):
        SomOfficeUser(123, 'something321@example.com', '1234G', 'ca_ES').create()
        mock_requests.post.assert_called_with(
            'https://somoffice.coopdevs.org/api/admin/import_user/',
            headers={'Content-Type': 'application/json'},
            auth=('user', 'password'),
            data=json.dumps({
                "customerCode": 123,
                "customerEmail": "something321@example.com",
                "customerUsername": "1234G",
                "customerLocale": "ca",
                "resetPassword": False
            })
        )

    @patch('odoo.addons.somconnexio.somoffice.user.requests', spec=['post'])
    def test_create_with_locale_es(self, mock_requests):
        SomOfficeUser(123, 'something321@example.com', '1234G', 'es_ES').create()
        mock_requests.post.assert_called_with(
            'https://somoffice.coopdevs.org/api/admin/import_user/',
            headers={'Content-Type': 'application/json'},
            auth=('user', 'password'),
            data=json.dumps({
                "customerCode": 123,
                "customerEmail": "something321@example.com",
                "customerUsername": "1234G",
                "customerLocale": "es",
                "resetPassword": False
            })
        )

    @patch.dict(os.environ, {
        'SOMOFFICE_RESET_PASSWORD': 'true'
    })
    @patch('odoo.addons.somconnexio.somoffice.user.requests', spec=['post'])
    def test_create_reset_password(self, mock_requests):
        SomOfficeUser(123, 'something321@example.com', '1234G', 'es_ES').create()
        mock_requests.post.assert_called_with(
            'https://somoffice.coopdevs.org/api/admin/import_user/',
            headers={'Content-Type': 'application/json'},
            auth=('user', 'password'),
            data=json.dumps({
                "customerCode": 123,
                "customerEmail": "something321@example.com",
                "customerUsername": "1234G",
                "customerLocale": "es",
                "resetPassword": True
            })
        )

    @patch.dict(os.environ, {
        'SOMOFFICE_RESET_PASSWORD': 'true'
    })
    @patch('odoo.addons.somconnexio.somoffice.user.requests', spec=['post'])
    def test_create_reset_password(self, mock_requests):
        with self.assertRaises(KeyError):
            SomOfficeUser(123, 'something321@example.com', '1234G', 'en_EN').create()
