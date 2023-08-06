from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    lc_number = fields.Char(
        string='LC Number',
    )
    po_box = fields.Char(
        string='PO BOX',
    )
    project_name  = fields.Char(
        string='Project Name',
        compute='compute_project_name'
    )
    date_of_issue = fields.Date(
        'Date of Issue'
    )
    no_show = fields.Char(
        'No Show',
        invisible=True
    )
    def compute_project_name(self):
        for rec in self:
            sale = self.env['sale.order'].search(
                [('name', '=', rec.invoice_origin)])
            if sale:
                rec.project_name = sale.subject
            else:
                rec.project_name = False
