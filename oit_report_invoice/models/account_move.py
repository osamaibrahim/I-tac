from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from googletrans import Translator



class AccountMove(models.Model):
    _inherit = "account.move"

    lc_number = fields.Char(string='LC Number')
    po_box = fields.Char(string='PO BOX')
    project_name  = fields.Char(string='Project Name', compute='compute_project_name')
    date_of_issue = fields.Date('Date of Issue')
    no_show = fields.Char('No Show')
    num_word = fields.Char(string="Amount Words:", compute='_compute_amount_in_word')
    sale_order_id = fields.Many2one(related='line_ids.sale_line_ids.order_id')
    purchase_order_id = fields.Many2one(related='line_ids.purchase_line_id.order_id')
    partner_name_ar = fields.Char(string='Partner Name Arabic', compute='compute_partner_name_ar')

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' فقط لاغير'

    @api.depends('partner_id')
    def compute_partner_name_ar(self):
        translator = Translator()
        for rec in self:
            if rec.partner_id and rec.partner_id.name:
                try:
                    # Translate the partner's name to Arabic
                    translated_name = translator.translate(rec.partner_id.name, src='en', dest='ar')
                    rec.partner_name_ar = translated_name.text
                except Exception as e:
                    # Handle translation errors
                    rec.partner_name_ar = "Translation Error"
                    # _logger.error(f"Error translating name to Arabic: {e}")
            else:
                rec.partner_name_ar = "No Name Provided"        

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
