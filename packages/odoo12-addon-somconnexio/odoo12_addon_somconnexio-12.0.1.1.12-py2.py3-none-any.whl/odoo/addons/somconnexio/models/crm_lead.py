from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    subscription_request_id = fields.Many2one(
        'subscription.request', 'Subscription Request'
    )
    iban = fields.Char(string="IBAN")

    mobile_lead_line_id = fields.Many2one(
        'crm.lead.line',
        compute='_compute_mobile_lead_line_id',
        string="Mobile Lead Line",
    )

    # TODO: To modify if in the future we can have more than one `mobile_lead_line_id`
    def _compute_mobile_lead_line_id(self):
        for crm_lead in self:
            for line in crm_lead.lead_line_ids:
                if line.mobile_isp_info:
                    crm_lead.mobile_lead_line_id = line
                    break

    def _ensure_crm_lead_iban_belongs_to_partner(self, crm_lead):
        partner_bank_ids = crm_lead.partner_id.bank_ids
        partner_iban_list = [bank.sanitized_acc_number for bank in partner_bank_ids]

        if crm_lead.iban and crm_lead.iban not in partner_iban_list:
            self.env['res.partner.bank'].create({
                'acc_type': 'iban',
                'acc_number': crm_lead.iban,
                'partner_id': crm_lead.partner_id.id
            })

    def action_set_won(self):
        for crm_lead in self:
            if crm_lead.iban:
                self._ensure_crm_lead_iban_belongs_to_partner(crm_lead)
        super(CrmLead, self).action_set_won()
