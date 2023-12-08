# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class res_company(models.Model):
    _inherit = "res.company"

    sale_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Sale')
    purchase_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Purchase')
    stock_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Stock')
    account_template = fields.Selection([
        ('fency', 'Fency'),
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('odoo_standard', 'Odoo Standard'),
    ], 'Account')


class account_invoice(models.Model):
    _inherit = "account.move"

    paypal_chk = fields.Boolean("Paypal")
    paypal_id = fields.Char("Paypal Id")
    shipping = fields.Float(compute='compute_final_total')
    other = fields.Float(compute='compute_final_total')
    final_total = fields.Float('Total After shipping and Other', compute='compute_final_total')

    # @api.depends('shipping')
    # def _compute_amount(self):
    #     super(account_invoice, self)._compute_amount()
    #     for rec in self:
    #         rec.ks_calculate_discount()

    # @api.multi
    def ks_calculate_discount(self):
        for rec in self:
            rec.amount_total = self.amount_untaxed + self.amount_tax + self.shipping
            # rec.update_move_lines()

    def update_move_lines(self):
        disc_amt = self.shipping
        in_draft_mode = self != self._origin
        total_amount = self.amount_untaxed + self.amount_tax + disc_amt
        if self.move_type == 'in_invoice':
            if self.account_shipping_id:
                ks_name = 'shipping'
                if in_draft_mode:
                    already_exists = self.line_ids.filtered(
                        lambda line: line.name and 'shipping' in line.name)
                    if already_exists:
                        already_exists.update({
                            'amount_currency': disc_amt,
                            'debit': disc_amt,
                        })
                    else:
                        create_method = self.env['account.move.line'].new
                        self.line_ids += create_method(
                            {
                                'move_name': self.name,
                                'name': ks_name,
                                'debit': disc_amt,
                                'currency_id': self.company_currency_id,
                                'amount_currency': disc_amt,
                                'credit': 0.0,
                                'account_id': self.account_shipping_id.id,
                                'move_id': self._origin,
                                'date': self.date,
                                'exclude_from_invoice_tab': True,
                                'partner_id': self.partner_id.id,
                                'company_id': self.company_id.id,
                            }
                        )

                terms_lines = self.line_ids.filtered(
                    lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                for line in terms_lines:
                    line.update({
                        'amount_currency': -total_amount ,
                        'credit': total_amount,
                    })

    # @api.model
    # def create(self, vals):
    #     doc = super(account_invoice, self).create(vals)
    #     doc.recompute_universal_discount_lines()
    #     return doc
    #
    # def recompute_universal_discount_lines(self):
    #     """This Function Create The General Entries for Universal Discount"""
    #     for rec in self:
    #         ks_name = 'names'
    #         amount = self.shipping
    #         self.update({'line_ids': [(0, 0, {'name': 'shipping',
    #                                           'account_id': rec.account_shipping_id.id,
    #                                           'debit': amount,
    #                                           'credit': 0.0,
    #                                           })]})
    #         self.update({'line_ids': [(0, 0, {'name': 'other',
    #                                           'account_id': rec.account_other_id.id,
    #                                           'debit': 0.0,
    #                                           'credit': amount,
    #                                           })]})
    #         for line in self.line_ids:
    #             if line.credit > 0.0:
    #                 line.credit = self.final_total

    def compute_final_total(self):
        for rec in self:
            if rec.invoice_origin:
                po = self.env['purchase.order'].search(
                    [('name', '=', rec.invoice_origin)])
                if po:
                    rec.shipping = po.shipping
                    rec.other = po.other
                    rec.final_total = po.final_total
                else:
                    rec.shipping = 0
                    rec.other = 0
                    rec.final_total = 0
            else:
                rec.shipping = 0
                rec.other = 0
                rec.final_total = 0

    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True
        return self.env.ref('bi_professional_reports_templates.custom_account_invoices').report_action(self)


class res_company(models.Model):
    _inherit = "res.company"

    bank_account_id = fields.Many2one('res.partner.bank', 'Bank Account')


class res_partner_bank(models.Model):
    _inherit = "res.partner.bank"

    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State')
    country_id = fields.Many2one('res.country', 'Country')
    swift_code = fields.Char('Swift Code')
    ifsc = fields.Char('IFSC')
    branch_name = fields.Char('Branch Name')


class sale_order(models.Model):
    _inherit = 'sale.order'

    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env.ref('bi_professional_reports_templates.custom_report_sale_order').report_action(self)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('bi_professional_reports_templates.custom_report_purchase_quotation').report_action(self)
