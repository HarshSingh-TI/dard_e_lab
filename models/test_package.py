from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
import logging
import base64

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
    cus_email = fields.Char(string="Email", required=True)
    
    list_price = fields.Float('Price', required=True)
    tester_id = fields.Many2one('res.partner', string='Sampler')
    Is_pathology = fields.Boolean(string="Is Pathology", default=False, required=True)
    home_sample = fields.Boolean(string="Home Sample", default=False, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            _l.info(val)

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

    # Method to send a report via email
    def send_email(self):
        pdf_report = self.env['ir.actions.report'].sudo()._render_qweb_pdf('Dard_e_Lab.pathology_lab_report_template', [self.id])[0]
        encoded_pdf = base64.b64encode(pdf_report)

        mail_values = {
            'subject': 'Pathology Test Notification',
            'body_html': '<p>Dear customer,</p><p>This is a test email from Pathways Pathology.</p>',
            'email_to': 'object.company_id.email',  
            'email_from': 'object.cus_email', 
            'auto_delete': True,  
            'attachment_ids': [(0, 0, {  
                'name': 'ReportAttachment.pdf',
                'type': 'binary',
                'datas': encoded_pdf.decode('utf-8'),
                'res_model': 'mail.mail',
                'res_id': 0,
                'mimetype': 'application/pdf'
            })]
        }
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
        return True

    # Method to send a custom test notification email
    def send_test_email(self):
        template = self.env.ref('Dard_e_Lab.email_template_pathology_test_notification')
        template.send_mail(self.id, force_send=True)

    # Method to schedule an appointment reminder
    def schedule_appointment_reminder(self):
        for record in self:
            reminder_date = record.create_date - timedelta(days=1)
            if reminder_date >= datetime.now():
                # Schedule reminder email
                self.env['mail.mail'].create({
                    'subject': 'Appointment Reminder',
                    'body_html': f'<p>Dear {record.cus_name},</p><p>Your test appointment is scheduled for {record.create_date}.</p>',
                    'email_to': record.cus_email,
                    'auto_delete': True,
                }).send()

    # Validation to check if the price is realistic
    @api.constrains('list_price')
    def _check_price(self):
        for record in self:
            if record.list_price < 10.0:
                raise exceptions.ValidationError("The price must be at least $10.00")
            

    @api.constrains('create_date')
    def _check_create_date(self):
        for record in self:
            if record.create_date and record.create_date < datetime.now():
                raise exceptions.ValidationError("The checkup date cannot be in the past.")
        

    
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
                
                
