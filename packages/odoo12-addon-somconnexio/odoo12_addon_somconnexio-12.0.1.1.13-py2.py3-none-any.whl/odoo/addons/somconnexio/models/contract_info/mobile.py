from odoo import models, fields


class MobileServiceContractInfo(models.Model):
    _name = 'mobile.service.contract.info'
    _inherit = 'base.service.contract.info'
    icc = fields.Char("ICC", required=True)
