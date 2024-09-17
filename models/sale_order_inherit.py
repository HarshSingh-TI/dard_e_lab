from odoo import models, fields
import logging
_l=logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    worker_id = fields.Many2one('res.partner', 'Worker')

    def action_confirm(self):
        """Override the confirmation action to show a wizard first."""

        
        self.action_cancel()

    def action_cancel(self):
        for rec in self:
            
            if self.env.context.get('from_button_click', False):
                _l.info("----------> Action cancel triggered from button click.")
                return {
            'type': 'ir.actions.act_window',
            'name': 'Confirm Sale Order',
            'res_model': 'sale.order.confirmation.wizard',
            'view_mode': 'form',
            'target': 'new',
           
            'context': {'default_worker_id': self.worker_id.id}, # Set default value for worker_id
            'from_button_click': True
        }
            else:
                rec.preferences = "Hell"
                
                _l.info("----------> Action cancel triggered programmatically.")

             

    def action_view_filtered_orders(self):
        """Action to apply default filters and group by."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',  # Display the tree view and form view
            'domain': [('state', '!=', 'draft')],  
            'context': {
                'group_by': 'partner_id',  # Group by partner_id
            },
        }        
