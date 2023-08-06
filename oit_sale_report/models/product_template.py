""" Initialize Product Template """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning

class NoModel(models.Model):
    _name = 'no.model'
    _description = 'Model No'
    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'Name must be unique'),
    ]

    name = fields.Char(
        required=True,
        translate=True,
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'
    volume = fields.Float('Volume', digits='Volume',compute='compute_new_volume')
    def compute_new_volume(self):
        for rec in self:
            rec.volume = rec.length * rec.width * rec.height

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    model_id = fields.Many2one(
        'no.model',
        string='No Model'
    )
    length = fields.Float(
        'Length'
    )
    width = fields.Float(
        'Width'
    )
    height = fields.Float(
        'Height'
    )
    ampere = fields.Float(
        'Ampere'
    )