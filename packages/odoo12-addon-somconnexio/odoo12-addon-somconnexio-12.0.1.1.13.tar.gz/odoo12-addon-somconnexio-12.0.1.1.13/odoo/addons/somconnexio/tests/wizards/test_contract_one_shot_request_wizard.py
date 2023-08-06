# -*- coding: utf-8 -*-

from datetime import datetime
from ..sc_test_case import SCTestCase


class TestContractOneShotRequestWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.start_date = datetime.strftime(datetime.today(), "%Y-%m-%d")
        self.masmovil_mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'icc': '123',
        })
        self.partner = self.browse_ref('base.partner_demo')
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract One Shot Request',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_masmovil"
            ),
            'mobile_contract_service_info_id': (
                self.masmovil_mobile_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.contract = self.env['contract.contract'].create(vals_contract)

        self.one_shot_product = self.ref(
            "somconnexio.EnviamentSIM"
            ),

    def test_wizard_one_shot_request_ok(self):

        self.assertEqual(len(self.contract.contract_line_ids), 0)

        wizard = self.env['contract.one.shot.request.wizard'].with_context(
            active_id=self.contract.id
        ).create({
            'start_date': self.start_date,
            'one_shot_product_id': self.one_shot_product,
        })
        wizard.button_add()

        self.assertEqual(len(self.contract.contract_line_ids), 1)
