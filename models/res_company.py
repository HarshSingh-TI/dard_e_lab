from odoo import models,fields,api

class resCompany(models.Model):
    _inherit = 'res.company'

    is_server_down=fields.Boolean(string="Go Offline")

    no_worker=fields.Boolean(string="Stop Tester Allotment")

    house_test= fields.Boolean(string="Stop Home Samples")

