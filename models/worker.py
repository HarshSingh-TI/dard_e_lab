from odoo import fields,models,api

class Workers(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(string='Name', required=True)
    image_128 = fields.Binary(String="Profile Photo")
    test_ids = fields.One2many('product.product', 'tester_id', string="Tests allotted")

