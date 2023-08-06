from odoo import models, fields, api
import json
from odoo.addons.queue_job.job import job
from odoo.addons.somconnexio.services.account_invoice_process import (
    AccountInvoiceProcess
)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    oc_taxes = fields.Char()
    oc_total = fields.Float()
    oc_untaxed = fields.Float()
    oc_total_taxed = fields.Float()

    @job
    def create_invoice(self, **params):
        service = AccountInvoiceProcess(self.env)
        service.create(**params)

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount',
                 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'date')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        if self.oc_untaxed:
            self.amount_untaxed = self.oc_untaxed
        else:
            self.amount_untaxed = sum(
                line.price_subtotal for line in self.invoice_line_ids
            )
        if self.oc_total_taxed:
            self.amount_tax = self.oc_total_taxed
        else:
            self.amount_tax = sum(
                round_curr(line.amount_total) for line in self.tax_line_ids
            )
        if self.oc_total:
            self.amount_total = self.oc_total
        else:
            self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if (
            self.currency_id and self.company_id and
            self.currency_id != self.company_id.currency_id
        ):
            currency_id = self.currency_id
            rate_date = self._get_currency_rate_date() or fields.Date.today()
            amount_total_company_signed = currency_id._convert(
                self.amount_total, self.company_id.currency_id,
                self.company_id, rate_date
            )
            amount_untaxed_signed = currency_id._convert(
                self.amount_untaxed, self.company_id.currency_id,
                self.company_id, rate_date
            )
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    @api.multi
    def compute_taxes(self):
        for invoice in self:
            oc_invoice = any([
                line.oc_amount_total
                for line in invoice.invoice_line_ids
            ])
            if not oc_invoice:
                super().compute_taxes()
                continue
            oc_taxes_parsed = json.loads(self.oc_taxes)
            for oc_tax in oc_taxes_parsed:
                taxes_amount = oc_tax['amountTax']
                base = oc_tax['amountWithoutTax']
                tax = self.env['account.tax'].search([
                    ('oc_code', '=', oc_tax['taxCode'])
                ])
                vals = {
                    'invoice_id': invoice.id,
                    'name': tax.name,
                    'tax_id': tax.id,
                    'amount': taxes_amount,
                    'base': base,
                    'manual': False,
                    'account_id': tax.account_id.id
                }
                self.env['account.invoice.tax'].create(vals)

    @api.multi
    def write(self, values):
        for invoice in self:
            if values.get('returned_payment'):
                activity_type = self.env.ref('somconnexio.return_activity_type_1')
                if invoice.returned_payment:
                    activity_type = self.env.ref('somconnexio.return_activity_type_n')
                self.env['mail.activity'].create({
                    'res_id': invoice.id,
                    'res_model_id': self.env['ir.model'].search(
                        [('model', '=', 'account.invoice')]
                    ).id,
                    'user_id': invoice.user_id.id,
                    'activity_type_id': activity_type.id,
                })

        return super(AccountInvoice, self).write(values)

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    def send_certificate_email(self, certificate_email_template, sub_reg_line):
        # we send the email with the certificate in attachment
        if self.company_id.send_certificate_email:
            certificate_email_template.sudo().send_mail(self.partner_id.id, False)

    @api.multi
    def get_invoice_pdf(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_invoice?invoice_number=%s' % self.name,
            'target': 'new',
        }
