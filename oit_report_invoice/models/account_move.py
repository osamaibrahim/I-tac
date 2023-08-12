from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime



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
    num_word = fields.Char(string="Amount Words:",
                           compute='_compute_amount_in_word',
                           ivvisible=True
                           )

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' فقط لاغير'

    @api.onchange('date_of_issue')
    def difference_date(self):
        for rec in self:
            if rec.date_of_issue and rec.invoice_date:
                fmt = '%Y-%m-%d'
                start_date = str(rec.invoice_date)
                end_date = str(rec.date_of_issue)
                d1 = datetime.strptime(start_date, fmt)
                d2 = datetime.strptime(end_date, fmt)
                if d2 < d1:
                    raise ValidationError("Invoice Date must be less than Date of Issue!")
    def compute_project_name(self):
        for rec in self:
            sale = self.env['sale.order'].search(
                [('name', '=', rec.invoice_origin)])
            if sale:
                rec.project_name = sale.subject
            else:
                rec.project_name = False
