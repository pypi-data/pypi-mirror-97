from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class ContractEmailChangeWizard(models.TransientModel):
    _name = 'contract.email.change.wizard'
    partner_id = fields.Many2one('res.partner')
    available_email_ids = fields.Many2many(
        'res.partner',
        string="Available Emails",
        compute="_load_available_email_ids"
    )
    contract_ids = fields.Many2many('contract.contract', string='Contracts')
    email_ids = fields.Many2many(
        'res.partner',
        string='Emails',
    )

    @api.multi
    @api.depends("partner_id")
    def _load_available_email_ids(self):
        if self.partner_id:
            self.available_email_ids = [
                (6, 0, self.partner_id.get_available_email_ids())
            ]

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['partner_id'] = self.env.context['active_id']
        return defaults

    @api.multi
    def button_change(self):
        self.ensure_one()
        for contract in self.contract_ids:
            message_partner = _("Email changed ({} --> {}) in partner's contract '{}'")
            self.partner_id.message_post(
                message_partner.format(
                    ', '.join([email.email for email in contract.email_ids]),
                    ', '.join([email.email for email in self.email_ids]),
                    contract.name
                )
            )
            message_contract = _("Contract email changed ({} --> {})")
            contract.message_post(
                message_contract.format(
                    ', '.join([email.email for email in contract.email_ids]),
                    ', '.join([email.email for email in self.email_ids]),
                )
            )
            contract.write(
                {'email_ids': [(6, 0, [email.id for email in self.email_ids])]}
            )
        return True
