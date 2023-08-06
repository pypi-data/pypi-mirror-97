from odoo.addons.component.core import Component

# 5 mins in seconds to delay the jobs
ETA = 300


class ContractLineListener(Component):
    _name = 'contract.line.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['contract.line']

    def on_record_create(self, record, fields=None):

        one_shot_products_categ_id_list = [
            self.env.ref('somconnexio.mobile_oneshot_service').id,
            self.env.ref('somconnexio.broadband_oneshot_service').id,
        ]
        service_products_categ_id_list = [
            self.env.ref('somconnexio.mobile_service').id,
            self.env.ref('somconnexio.broadband_fiber_service').id,
            self.env.ref('somconnexio.broadband_adsl_service').id,
        ]

        if record.product_id.categ_id.id in one_shot_products_categ_id_list:
            self.env['contract.contract'].with_delay(
                priority=50,
                eta=ETA
            ).add_one_shot(
                record.contract_id.id,
                record.product_id.default_code
            )

        elif record.product_id.categ_id.id in service_products_categ_id_list:
            self.env['contract.contract'].with_delay(
                priority=50,
                eta=ETA
            ).create_new_service(
                record.contract_id.id,
                record
            )

    def on_record_write(self, record, fields=None):
        if record.date_end:
            self.env['contract.contract'].with_delay(
                priority=50,
                eta=ETA
            ).terminate_service(
                record.contract_id.id,
                record
            )
