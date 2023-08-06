from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re
from odoo.addons.somconnexio.services import schemas

mac_regex = schemas.S_ADSL_CONTRACT_SERVICE_INFO_CREATE[
    'router_mac_address'
]['regex']


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    router_mac_address = fields.Char('Router MAC Address')

    _sql_constraints = [
        ('router_mac_address_uniq', 'unique (router_mac_address)',
         'The router MAC address must be unique !'
         ),
    ]

    @api.model
    def check_mac_address(self, mac_address):
        return re.match(mac_regex, mac_address.upper())

    @api.one
    @api.constrains('router_mac_address')
    def validator_mac_address(self):
        if not self.env['stock.production.lot'].check_mac_address(
            self.router_mac_address
        ):
            raise ValidationError("Not valid MAC Address")

    def name_get(self):
        res = super().name_get()
        result = []
        for elem in res:
            spl_id = elem[0]
            spl = self.browse(spl_id)
            if spl.router_mac_address:
                result.append((spl_id, elem[1]+" / "+spl.router_mac_address))
            else:
                result.append((spl_id, elem[1]))
        return result

    @api.multi
    def write(self, values):
        if 'router_mac_address' in values:
            values['router_mac_address'] = values.get('router_mac_address', '').upper()

        return super().write(values)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if 'router_mac_address' in values:
                values['router_mac_address'] = values['router_mac_address'].upper()
        return super().create(vals_list)
