from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class CRMLeadLineTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.crm_lead_id = self.env['crm.lead'].create(
            [{'name': 'Test Lead'}]
        )[0].id
        self.crm_lead_line_args = {
            'name': '666666666',
            'product_id': '666666666',
            'mobile_isp_info': None,
            'broadband_isp_info': None,
        }
        self.mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'new',
        })
        self.broadband_isp_info = self.env['broadband.isp.info'].create({
            'phone_number': '666666666',
            'type': 'new',
        })

        broadband_adsl_product_tmpl_args = {
            'name': 'ADSL 20Mb',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_adsl_service')
        }
        product_adsl_broadband_tmpl = self.env['product.template'].create(
            broadband_adsl_product_tmpl_args
        )
        self.product_broadband_adsl = product_adsl_broadband_tmpl.product_variant_id

        mobile_product_tmpl_args = {
            'name': 'Sense minutes',
            'type': 'service',
            'categ_id': self.ref('somconnexio.mobile_service')
        }
        product_mobile_tmpl = self.env['product.template'].create(
            mobile_product_tmpl_args
        )
        self.product_mobile = product_mobile_tmpl.product_variant_id

    def test_mobile_lead_line_creation_ok(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'mobile_isp_info': self.mobile_isp_info.id,
            'product_id': self.product_mobile.id
        })

        mobile_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )
        self.assertTrue(mobile_crm_lead_line.id)

    def test_broadband_lead_line_creation_ok(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'broadband_isp_info': self.broadband_isp_info.id,
            'product_id': self.product_broadband_adsl.id
        })

        broadband_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )
        self.assertTrue(broadband_crm_lead_line.id)

    def test_broadband_lead_line_creation_without_bradband_isp_info(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'product_id': self.product_broadband_adsl.id
        })

        self.assertRaises(
            ValidationError,
            self.env['crm.lead.line'].create,
            [crm_lead_line_args_copy]
        )

    def test_mobile_lead_line_creation_without_mobile_isp_info(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'product_id': self.product_mobile.id
        })

        self.assertRaises(
            ValidationError,
            self.env['crm.lead.line'].create,
            [crm_lead_line_args_copy]
        )
