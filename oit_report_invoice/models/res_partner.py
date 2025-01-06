from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    name_ar = fields.Char(string='Name Arabic')