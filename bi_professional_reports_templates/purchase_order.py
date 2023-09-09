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

    def add_shipping_other(self):
        """ Add Shipping Other """
        for rec in self:
            lines = rec.order_line.filtered(lambda x: x.is_shipping_other)
            if lines:
                lines.unlink()

            self.env['purchase.order.line'].create({
                'product_id': rec.company_id.shipping_product_id.id,
                'product_qty': 1,
                'name': 'Shipping Amount',
                'price_unit': rec.shipping,
                'is_shipping_other': True,
                'order_id': rec.id,
            })

            self.env['purchase.order.line'].create({
                'product_id': rec.company_id.other_product_id.id,
                'product_qty': 1,
                'name': 'Other Amount',
                'price_unit': rec.other,
                'is_shipping_other': True,
                'order_id': rec.id,
            })



class PurchaseOrderLine(models.Model):
    """
        Inherit Account Move Line:
         -
    """
    _inherit = 'purchase.order.line'

    is_shipping_other = fields.Boolean()
