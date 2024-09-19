from odoo import models, fields, api

class resConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    


    is_server_down=fields.Boolean(string="Go Offline", config_parameter='Dad_e_Lab.is_server_down')

    no_worker=fields.Boolean(string="Stop Tester Allotment", config_parameter='Dard_e_Lab.no_worker')

    house_test= fields.Boolean(string="Stop Home Samples", config_parameter='Dard_e_Lab.house_test')