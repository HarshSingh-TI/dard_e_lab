from odoo import models,fields


class SaleOrder(models.Model):
    _inherit='sale.order'

    worker_id=fields.Many2one('res.partner','Worker')


