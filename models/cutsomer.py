from odoo import fields,models,api

class Customer(models.Model):
    _inherit = 'res.partner'
