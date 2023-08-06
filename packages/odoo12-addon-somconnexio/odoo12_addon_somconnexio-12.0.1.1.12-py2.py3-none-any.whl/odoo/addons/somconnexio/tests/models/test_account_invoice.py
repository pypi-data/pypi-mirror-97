from ..sc_test_case import SCTestCase
from datetime import date


class AccountInvoiceTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        date_invoice = date(2021, 1, 31)
        partner = self.browse_ref('easy_my_coop.res_partner_cooperator_1_demo')
        self.user = self.browse_ref('somconnexio.cesar')
        self.invoice = self.env['account.invoice'].create({
            'partner_id': partner.id,
            'date_invoice': date_invoice
        })

    def test_activity_creation_when_returned_payment(self):
        self.invoice.returned_payment = True
        activity_type_1 = self.ref('somconnexio.return_activity_type_1')
        account_invoice_model = self.env['ir.model'].search(
            [('model', '=', 'account.invoice')]
        )
        self.assertTrue(
            self.env['mail.activity'].search([
                ('res_id', '=', self.invoice.id),
                ('res_model_id', '=', account_invoice_model.id),
                ('activity_type_id', '=', activity_type_1)
            ])
        )

    def test_no_activity_creation_when_missing_returned_payment(self):
        self.invoice.returned_payment = False
        self.invoice.reference = "1234"
        activity_type_1 = self.ref('somconnexio.return_activity_type_1')
        account_invoice_model = self.env['ir.model'].search(
            [('model', '=', 'account.invoice')]
        )
        self.assertFalse(
            self.env['mail.activity'].search([
                ('res_id', '=', self.invoice.id),
                ('res_model_id', '=', account_invoice_model.id),
                ('activity_type_id', '=', activity_type_1)
            ])
        )

    def test_activity_creation_type_n_when_returned_payment_again(self):
        self.invoice.returned_payment = True
        self.invoice.returned_payment = True
        activity_type_n = self.ref('somconnexio.return_activity_type_n')
        account_invoice_model = self.env['ir.model'].search(
            [('model', '=', 'account.invoice')]
        )
        self.assertTrue(
            self.env['mail.activity'].search([
                ('res_id', '=', self.invoice.id),
                ('res_model_id', '=', account_invoice_model.id),
                ('activity_type_id', '=', activity_type_n)
            ])
        )
