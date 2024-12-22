from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    email_body_template = fields.Text(string='Email Body Template')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        parameter_obj = self.env['ir.config_parameter'].sudo()
        parameter_obj.set_param('oit_sale_report.email_body_template', self.email_body_template)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        parameter_obj = self.env['ir.config_parameter'].sudo()
        email_body_template = parameter_obj.get_param('oit_sale_report.email_body_template')
        res.update(
            email_body_template=email_body_template
        )
        return res
