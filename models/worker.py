from odoo import fields,models,api
import logging
_l=logging.getLogger(__name__)


class Workers(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(string='Name', required=True)
    image_128 = fields.Binary(String="Profile Photo")
    test_ids = fields.One2many('product.product', 'tester_id', string="Tests allotted")



    @api.model_create_multi
    def create(self,vals_list):
        for val in vals_list:
            _l.info(val)
            no_worker = self.env['ir.config_parameter'].sudo().get_param('Dad_e_Lab.no_worker')
        
            if no_worker:
                raise models.ValidationError("The sots are full. No tester is free right now. Sorry for the inconvenience")
                
        return super().create(vals_list)

