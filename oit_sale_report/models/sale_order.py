""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    email_body_template = fields.Text(string='Email Body Template', compute='compute_email_body_template')
    subject = fields.Char('Subject')
    child_ids = fields.Many2many('res.partner', compute='compute_child_ids')
    attention_id = fields.Many2one('res.partner',)
    notes = fields.Text('Notes')
    department_id = fields.Many2one('hr.department')

    @api.depends('partner_id')
    def compute_child_ids(self):
        for rec in self:
            if rec.partner_id.child_ids:
                for record in rec.partner_id.child_ids:
                    rec.child_ids = [(4, record.id)]
            else:
                rec.child_ids = False

    def compute_email_body_template(self):
        for rec in self:
            email_body_template = self.env['ir.config_parameter'].sudo().get_param(
                'oit_sale_report.email_body_template')
            if email_body_template:
                rec.email_body_template = email_body_template
            else:
                rec.email_body_template = False

