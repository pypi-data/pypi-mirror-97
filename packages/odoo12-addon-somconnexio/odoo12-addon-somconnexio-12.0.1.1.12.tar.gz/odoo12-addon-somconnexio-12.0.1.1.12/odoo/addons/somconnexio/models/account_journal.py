from odoo import models, fields


class account_journal(models.Model):
    _inherit = "account.journal"
    name = fields.Char(translate=True)
