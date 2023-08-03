""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    subject = fields.Char(
        'Subject'
    )
    child_ids = fields.Many2many(
        'res.partner',
        compute='compute_child_ids'
    )
    notes = fields.Text(
        'Notes'
    )

    def compute_child_ids(self):
        for rec in self:
            if rec.partner_id.child_ids:
                for record in rec.partner_id.child_ids:
                    rec.child_ids = [(4, record.id)]
            else:
                rec.child_ids = False


