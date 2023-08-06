# -*- coding: utf-8 -*-
from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class TestCreateLeadfromPartnerWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner = self.browse_ref('somconnexio.res_partner_2_demo')

    def test_create_new_mobile_lead(self):
        wizard = self.env['partner.create.lead.wizard'].with_context(
            active_id=self.partner.id
        ).create({
            'opportunity': 'test new mobile with invoice address',
            'bank_id': self.partner.bank_ids.id,
            'email_id': self.partner.id,
            'phone_contact': '888888888',
            'product_id': self.ref('somconnexio.SenseMinuts2GB'),
            'service_type': 'mobile',
            'icc': '666',
            'type': 'new',
            'delivery_street': 'Principal A',
            'delivery_zip_code': '08027',
            'delivery_city': 'Barcelona',
            'delivery_state_id': self.ref('base.state_es_b'),
            'delivery_country_id': self.ref('base.es'),
            'invoice_street': 'Principal B',
            'invoice_zip_code': '08015',
            'invoice_city': 'Barcelona',
            'invoice_state_id': self.ref('base.state_es_b'),
            'invoice_country_id': self.ref('base.es'),
        })

        crm_lead_action = wizard.create_lead()
        crm_lead = self.env["crm.lead"].browse(crm_lead_action["res_id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertEquals(crm_lead.name, "test new mobile with invoice address")
        self.assertEquals(crm_lead.partner_id, self.partner)
        self.assertEquals(
            crm_lead.iban,
            self.partner.bank_ids.sanitized_acc_number
        )
        self.assertEquals(crm_lead.email_from, self.partner.email)
        self.assertEquals(crm_lead_line.mobile_isp_info.icc, '666')
        self.assertEquals(crm_lead_line.mobile_isp_info.type, 'new')
        self.assertEquals(
            crm_lead_line.product_id,
            self.browse_ref('somconnexio.SenseMinuts2GB')
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_street,
            'Principal A'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_zip_code,
            '08027'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_country_id,
            self.browse_ref('base.es')
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_street,
            'Principal B'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_zip_code,
            '08015'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_country_id,
            self.browse_ref('base.es')
        )

    def test_create_portability_mobile_lead(self):
        wizard = self.env['partner.create.lead.wizard'].with_context(
            active_id=self.partner.id
        ).create({
            'opportunity': 'test portability mobile',
            'bank_id': self.partner.bank_ids.id,
            'email_id': self.partner.id,
            'phone_contact': '888888888',
            'product_id': self.ref('somconnexio.SenseMinuts2GB'),
            'service_type': 'mobile',
            'icc': '666',
            'type': 'portability',
            'previous_contract_type': 'contract',
            'phone_number': '666666666',
            'donor_icc': '3333',
            'previous_mobile_provider': self.ref('somconnexio.previousprovider4'),
            'previous_owner_vat_number': '52736216E',
            'previous_owner_first_name': 'Firstname test',
            'previous_owner_name': 'Lastname test',
            'delivery_street': 'Principal A',
            'delivery_zip_code': '08027',
            'delivery_city': 'Barcelona',
            'delivery_state_id': self.ref('base.state_es_b'),
            'delivery_country_id': self.ref('base.es'),
        })

        crm_lead_action = wizard.create_lead()
        crm_lead = self.env["crm.lead"].browse(crm_lead_action["res_id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertEquals(crm_lead.name, "test portability mobile")
        self.assertEquals(crm_lead.partner_id, self.partner)
        self.assertEquals(
            crm_lead.iban,
            self.partner.bank_ids.sanitized_acc_number
        )
        self.assertEquals(crm_lead.email_from, self.partner.email)
        self.assertEquals(
            crm_lead_line.product_id,
            self.browse_ref('somconnexio.SenseMinuts2GB')
        )
        self.assertEquals(crm_lead_line.mobile_isp_info.icc, '666')
        self.assertEquals(crm_lead_line.mobile_isp_info.type, 'portability')
        self.assertEquals(
            crm_lead_line.mobile_isp_info.previous_contract_type,
            'contract'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.phone_number,
            '666666666'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.icc_donor,
            '3333'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.previous_provider,
            self.browse_ref('somconnexio.previousprovider4')
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.previous_owner_vat_number,
            '52736216E'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.previous_owner_first_name,
            'Firstname test'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.previous_owner_name,
            'Lastname test'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_street,
            'Principal A'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_zip_code,
            '08027'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_country_id,
            self.browse_ref('base.es')
        )

    def test_create_new_BA_lead(self):

        wizard = self.env['partner.create.lead.wizard'].with_context(
            active_id=self.partner.id
        ).create({
            'opportunity': 'test new BA',
            'bank_id': self.partner.bank_ids.id,
            'email_id': self.partner.id,
            'phone_contact': '888888888',
            'product_id': self.ref('somconnexio.Fibra600Mb'),
            'service_type': 'BA',
            'type': 'new',
            'delivery_street': 'Principal A',
            'delivery_zip_code': '08027',
            'delivery_city': 'Barcelona',
            'delivery_state_id': self.ref('base.state_es_b'),
            'delivery_country_id': self.ref('base.es'),
            'service_street': 'Principal B',
            'service_zip_code': '00123',
            'service_city': 'Barcelona',
            'service_state_id': self.ref('base.state_es_b'),
            'service_country_id': self.ref('base.es'),
        })

        crm_lead_action = wizard.create_lead()
        crm_lead = self.env["crm.lead"].browse(crm_lead_action["res_id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertEquals(crm_lead.name, "test new BA")
        self.assertEquals(crm_lead.partner_id, self.partner)
        self.assertEquals(
            crm_lead.iban,
            self.partner.bank_ids.sanitized_acc_number
        )
        self.assertEquals(crm_lead.email_from, self.partner.email)
        self.assertEquals(
            crm_lead_line.product_id,
            self.browse_ref('somconnexio.Fibra600Mb')
        )
        self.assertEquals(crm_lead_line.broadband_isp_info.type, 'new')
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_street,
            'Principal B'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_zip_code,
            '00123'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_country_id,
            self.browse_ref('base.es')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_street,
            'Principal A'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_zip_code,
            '08027'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_country_id,
            self.browse_ref('base.es')
        )

    def test_create_portability_BA_lead(self):
        wizard = self.env['partner.create.lead.wizard'].with_context(
            active_id=self.partner.id
        ).create({
            'opportunity': 'test BA portability',
            'bank_id': self.partner.bank_ids.id,
            'email_id': self.partner.id,
            'phone_contact': '888888888',
            'product_id': self.ref('somconnexio.Fibra600Mb'),
            'service_type': 'BA',
            'type': 'portability',
            'previous_owner_vat_number': '52736216E',
            'previous_owner_first_name': 'Test',
            'previous_owner_name': 'Test',
            'keep_landline': True,
            'previous_BA_service': "adsl",
            'previous_BA_provider': self.ref('somconnexio.previousprovider3'),
            'service_street': 'Principal A',
            'service_zip_code': '00123',
            'service_city': 'Barcelona',
            'service_state_id': self.ref('base.state_es_b'),
            'service_country_id': self.ref('base.es'),
            'delivery_street': 'Principal B',
            'delivery_zip_code': '08027',
            'delivery_city': 'Barcelona',
            'delivery_state_id': self.ref('base.state_es_b'),
            'delivery_country_id': self.ref('base.es'),
        })

        crm_lead_action = wizard.create_lead()
        crm_lead = self.env["crm.lead"].browse(crm_lead_action["res_id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertEquals(crm_lead.name, "test BA portability")
        self.assertEquals(crm_lead.partner_id, self.partner)
        self.assertEquals(
            crm_lead.iban,
            self.partner.bank_ids.sanitized_acc_number
        )
        self.assertEquals(crm_lead.email_from, self.partner.email)
        self.assertEquals(
            crm_lead_line.product_id,
            self.browse_ref('somconnexio.Fibra600Mb')
        )
        self.assertEquals(crm_lead_line.broadband_isp_info.type, 'portability')
        self.assertTrue(crm_lead_line.broadband_isp_info.keep_phone_number)
        self.assertEquals(
            crm_lead_line.broadband_isp_info.previous_provider,
            self.browse_ref('somconnexio.previousprovider3')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.previous_service,
            'adsl'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_street,
            'Principal A'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_zip_code,
            '00123'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_country_id,
            self.browse_ref('base.es')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_street,
            'Principal B'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_zip_code,
            '08027'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.delivery_country_id,
            self.browse_ref('base.es')
        )

    def test_create_portability_mobile_without_phone_number(self):
        wizard = self.env['partner.create.lead.wizard'].with_context(
            active_id=self.partner.id
        ).create({
            'opportunity': 'test portability mobile',
            'bank_id': self.partner.bank_ids.id,
            'email_id': self.partner.id,
            'phone_contact': '888888888',
            'product_id': self.ref('somconnexio.SenseMinuts2GB'),
            'service_type': 'mobile',
            'icc': '666',
            'type': 'portability',
            'previous_contract_type': 'contract',
            'donor_icc': '3333',
            'previous_mobile_provider': self.ref('somconnexio.previousprovider4'),
            'previous_owner_vat_number': '52736216E',
            'previous_owner_first_name': 'Firstname test',
            'previous_owner_name': 'Lastname test',
            'delivery_street': 'Principal A',
            'delivery_zip_code': '08027',
            'delivery_city': 'Barcelona',
            'delivery_state_id': self.ref('base.state_es_b'),
            'delivery_country_id': self.ref('base.es'),
        })

        self.assertRaises(
            ValidationError,
            wizard.create_lead
        )
