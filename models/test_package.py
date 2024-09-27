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

    cus_name = fields.Char(string="Patient Name", required=True)
    cus_add = fields.Char(string="Address", required=True)
    cus_email = fields.Char(string="email", required=True)
    
    list_price = fields.Float('Price', required=True)
    tester_id = fields.Many2one('res.partner', string='Sampler')
    Is_pathology = fields.Boolean(string="is pathology", default=False, required=True)
    
    home_sample = fields.Boolean(string="Home Sample", default=False, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            _l.info(val)
            # is_server_down = self.env['ir.config_parameter'].sudo().get_param('Dad_e_Lab.is_server_down')
            # house_test = self.env['ir.config_parameter'].sudo().get_param('Dard_e_Lab.house_test')

            
            settings = self.env['res.config.settings'].search([], limit=1)
            is_server_down = settings and settings.is_server_down
            house_test = settings and settings.house_test


            if is_server_down:
                raise models.ValidationError("The server is down. Bookings cannot be done right now. Sorry for the inconvenience")
            
            if not val.get('reference') or val['reference'] == 'New':
                val['reference'] = self.env['ir.sequence'].next_by_code('product.product')

            if house_test and house_test == 'True':
                val['home_sample'] = False 

            if val['home_sample']:
                val['standard_price'] = val['list_price'] + (val['list_price']*0.15) + 100.0 
            else:
                val['standard_price'] = val['list_price']+ (val['list_price']*0.15)

        return super().create(vals_list)
    


    def send_email(self):

        mail_values = {
            'subject': 'Pathology Test Notification',
            'body_html': '<p>Dear customer,</p><p>This is a test email from Pathways Pathology.</p>',
            'email_to': 'object.company_id.email',  
            'email_from': 'object.cus_email', 
        }
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
    


    def send_test_email(self):
        template = self.env.ref('Dard_e_Lab.email_template_pathology_test_notification')
        template.send_mail(self.id, force_send=True)


    
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
                
                
