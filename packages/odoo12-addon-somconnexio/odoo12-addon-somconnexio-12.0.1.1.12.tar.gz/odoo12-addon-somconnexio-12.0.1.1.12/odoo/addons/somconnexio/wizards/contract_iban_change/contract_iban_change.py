from odoo import api, fields, models, _


class ContractIbanChangeWizard(models.TransientModel):
    _name = 'contract.iban.change.wizard'
    partner_id = fields.Many2one('res.partner')
    contract_ids = fields.Many2many('contract.contract', string='Contracts')
    account_banking_mandate_id = fields.Many2one(
        'account.banking.mandate', 'Banking mandate'
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['partner_id'] = self.env.context['active_id']
        return defaults

    @api.multi
    def button_change(self):
        self.ensure_one()

        message_contract = _("Contract IBAN changed from {} to {}")
        contract_names = []
        for contract in self.contract_ids:
            contract.message_post(
                message_contract.format(
                    contract.mandate_id.partner_bank_id.acc_number,
                    self.account_banking_mandate_id.partner_bank_id.acc_number,
                )
            )
            contract_names.append(contract.name)

        message_partner = _("IBAN changed from {} to {} in partner's contract/s '{}'")
        self.partner_id.message_post(
            message_partner.format(
                contract.mandate_id.partner_bank_id.acc_number,
                self.account_banking_mandate_id.partner_bank_id.acc_number,
                ", ".join(contract_names)
            )
        )

        self.contract_ids.write({'mandate_id': self.account_banking_mandate_id.id})

        return True
