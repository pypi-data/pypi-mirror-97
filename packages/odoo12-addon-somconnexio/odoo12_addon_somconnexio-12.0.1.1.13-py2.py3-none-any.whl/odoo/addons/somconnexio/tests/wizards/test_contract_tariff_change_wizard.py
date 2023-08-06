# -*- coding: utf-8 -*-

from datetime import date
from ..sc_test_case import SCTestCase


class TestContractTariffChangeWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

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
        product_ref = self.browse_ref('somconnexio.150Min1GB')
        product = self.env["product.product"].search(
            [('default_code', '=', product_ref.default_code)]
        )
        contract_line = {
            "name": product.name,
            "product_id": product.id,
            "date_start": "2020-01-01 00:00:00"
        }
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
            'bank_id': self.partner.bank_ids.id,
            'contract_line_ids': [
                (0, False, contract_line)
            ]
        }
        self.contract = self.env['contract.contract'].create(vals_contract)

        self.new_tariff_product_id = self.ref("somconnexio.150Min2GB")

    def test_wizard_tariff_change_ok(self):
        self.assertEqual(self.contract.current_tariff_contract_line.product_id.id,
                         self.ref('somconnexio.150Min1GB'))
        start_date = date.today()

        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract.id
        ).create({
            'start_date': start_date,
            'new_tariff_product_id': self.new_tariff_product_id,
        })
        wizard.button_change()

        self.assertTrue(self.contract.contract_line_ids[0].date_end)
        self.assertFalse(self.contract.contract_line_ids[1].date_end)
        self.assertEqual(self.contract.contract_line_ids[1].date_start,
                         start_date)
        self.assertEqual(self.contract.contract_line_ids[1].product_id.id,
                         self.new_tariff_product_id)
