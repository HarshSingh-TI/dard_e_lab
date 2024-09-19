from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
import logging

_l = logging.getLogger(__name__)

class TestPackage(models.Model):
    _inherit = 'product.product'

    create_date = fields.Datetime(string='Checkup Date', help='Date and time when you can have your checkup', readonly=False)
    reference = fields.Char(string="Test Package Reference", default="New")
    type = fields.Selection([
        ('blood', 'Blood Tests'),
        ('urine', 'Urine Tests'),
        ('stool', 'Stool Tests'),
        ('imaging', 'Imaging Tests'),
        ('genetic', 'Genetic Tests'),
        ('biopsy', 'Biopsy')
    ], string='Checkup Type', required=True, default='blood')
    
    list_price = fields.Float('Price', required=True)
    tester_id = fields.Many2one('res.partner', string='Sampler')
    Is_pathology = fields.Boolean(string="is pathology", default=False, required=True)
    
    home_sample = fields.Boolean(string="Home Sample", default=False, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            _l.info(val)
            is_server_down = self.env['ir.config_parameter'].sudo().get_param('Dad_e_Lab.is_server_down')
            house_test = self.env['ir.config_parameter'].sudo().get_param('Dard_e_Lab.house_test')

            if is_server_down:
                raise models.ValidationError("The server is down. Bookings cannot be done right now. Sorry for the inconvenience")
            
            if not val.get('reference') or val['reference'] == 'New':
                val['reference'] = self.env['ir.sequence'].next_by_code('product.product')

            if house_test and house_test == 'True':
                val['home_sample'] = False  # Disable home sample if house_test is true

            if val['home_sample']:
                val['standard_price'] = val['list_price'] + 100.0
            else:
                val['standard_price'] = val['list_price']

        return super().create(vals_list)

    
    # @api.model
    # def write(self,vals_list):
    #     self.ensure_one()
        
    #     for rec in self:
    #         if rec.home_sample:
    #             rec.standard_price+=rec.lst_price+100.0
               
    #     return super().write(vals_list)


    

    # @api.constrains('create_date')
    # def _check_create_date(self):
    #     for rec in self:
    #         if rec.create_date:
    #             current_date = datetime.now()
               
    #             if rec.create_date < current_date:
    #                 raise exceptions.ValidationError("The checkup date cannot be in the past.")
                
                
