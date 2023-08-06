from odoo.addons.component.core import Component

# 5 mins in seconds to delay the jobs
ETA = 300


class Contract(Component):
    _name = 'contract.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['contract.contract']

    def on_record_create(self, record, fields=None):
        self.env['contract.contract'].with_delay(priority=0).create_subscription(
            record.id
        )

    def on_record_write(self, record, fields=None):
        if 'is_terminated' in fields and record.is_terminated:
            self.env['contract.contract'].with_delay(
                priority=50,
                eta=ETA
            ).terminate_subscription(
                record.id
            )
        if 'mandate_id' in fields or 'email_ids' in fields:
            self.env['contract.contract'].with_delay(
                priority=50,
                eta=ETA
            ).update_subscription(
                record.id
            )
