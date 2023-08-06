import json
from ..common_service import BaseEMCRestCaseAdmin


class TestDiscoveryhannelController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()

    def test_route_search_without_filter(self):
        url = "/api/discovery-channel"

        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertIn('discovery_channels', content)
        self.assertEqual(len(content['discovery_channels']), 8)
