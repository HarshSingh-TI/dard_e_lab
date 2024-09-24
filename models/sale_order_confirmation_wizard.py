from odoo import models, fields, api
import logging

_l = logging.getLogger(__name__)


class SaleOrderCancelWizard(models.TransientModel):
    _name = 'sale.order.confirmation.wizard'
    _description = 'Sale Order Cancel Wizard'

    worker_id = fields.Many2one('res.partner', 'Worker', default=lambda self: self.env.context.get('default_worker_id'))

    def validate_action_confirm(self):
        ids = self.env.context.get('active_ids', [])
        _l.info(f"------------------> Active ids : {ids}")
        
        sale_ids = self.env['sale.order'].browse(ids)
        _l.info(f"------------------> sale ids : {sale_ids}")
        
        
        sale_ids = sale_ids.with_context(validate_not_click=False)
        _l.info(f"----------> wizard context : {self._context}")
        
        return sale_ids.action_cancel()
