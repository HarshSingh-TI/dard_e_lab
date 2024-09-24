from odoo import models, fields, api

class resConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    


    is_server_down=fields.Boolean(string="Go Offline", related='company_id.is_server_down', readonly=False)

    no_worker=fields.Boolean(string="Stop Tester Allotment", related='company_id.no_worker', readonly=False)

    house_test= fields.Boolean(string="Stop Home Samples", related='company_id.house_test', readonly=False)