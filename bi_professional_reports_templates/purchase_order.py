""" Initialize Purchase Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class PurchaseOrder(models.Model):
    """
        Inherit Purchase Order:
         - 
    """
    _inherit = 'purchase.order'
    
    fob = fields.Char(
        'F.O.B.'
    )
    ship_via = fields.Char()
    shipping = fields.Float()
    other = fields.Float()
    final_total = fields.Float('Total After shipping and Other',compute='compute_final_total')
    def compute_final_total(self):
        for rec in self:
            rec.final_total = rec.amount_total + rec.shipping + rec.other