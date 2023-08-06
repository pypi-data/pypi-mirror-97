from odoo import models, fields


class CoopAgreement(models.Model):
    _name = 'coop.agreement'
    _description = "Cooperative agreement"
    _rec_name = 'code'
    partner_id = fields.Many2one('res.partner',
                                 required=True,
                                 string='Cooperator')
    products = fields.Many2many(comodel_name='product.template',
                                string='Products',
                                required=True,
                                help="Products available for the partners sponsored"
                                " by that cooperative.")
    code = fields.Char(string='Code', required=True)
