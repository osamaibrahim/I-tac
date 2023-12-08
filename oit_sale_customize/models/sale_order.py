""" Initialize Model """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('approved', 'Approved'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ],
    )
    is_approved = fields.Boolean(
        copy=0
    )
    
    def action_approve(self):
        """ Action Approve """
        for rec in self:
            rec.state = 'approved'
            rec.is_approved = True

    def action_quotation_send(self):
        """ Override action_quotation_send """
        res = super(SaleOrder, self).action_quotation_send()
        for rec in self:
            if not rec.is_approved:
                raise ValidationError('Quotation must be approved first !')
            rec.state = 'sent'
        return res