from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    reference = fields.Char(
        string='Reference',
        compute='_compute_reference',
        readonly=True,
        store=False
    )
    activity_type_name = fields.Char(
        related="activity_type_id.name"
    )
    date_done = fields.Date(readonly=False)
    location = fields.Char()
    partner_id = fields.Many2one(
        'res.partner',
        compute='_compute_res_partner', readonly=True, store=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if res.get('res_model') == 'res.partner':
            partner = self.env['res.partner'].browse(res.get('res_id'))
            if partner.parent_id:
                raise UserError(_("It is not possible to create an activity from a child partner. Do it through its parent instead"))  # noqa
        return res

    @api.depends('res_model', 'res_id')
    def _compute_reference(self):
        for res in self:
            res.reference = "%s,%s" % (res.res_model, res.res_id)

    @api.depends('res_model', 'res_id')
    def _compute_res_partner(self):
        for res in self:
            if res.res_model == 'contract.contract':
                contract = self.env['contract.contract'].browse(res.res_id)
                res.partner_id = contract.partner_id
            elif res.res_model == 'res.partner':
                res.partner_id = self.env['res.partner'].browse(res.res_id)
            else:
                res.partner_id = False

    def action_reopen(self):
        self.ensure_one()
        self.date_done = False
        self.done = False

        message = _("Activity '{}' reopened on date {}")
        record = self.env[self.res_model].browse(self.res_id)
        record.message_post(
            message.format(
                self.summary,
                date.today().strftime("%d-%m-%Y")
            )
        )
