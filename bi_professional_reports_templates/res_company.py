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
    final_total = fields.Float('Total After shipping and Other',compute='compute_final_total')


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
    shipping_product_id = fields.Many2one(
        'product.product'
    )
    other_product_id = fields.Many2one(
        'product.product'
    )


class ResConfigSettings(models.TransientModel):
    """ Inherit res.config.setting model to add Res configuration"""
    _inherit = 'res.config.settings'
    shipping_product_id = fields.Many2one(
        'product.product',
        related='company_id.shipping_product_id',
        readonly=False
    )
    other_product_id = fields.Many2one(
        'product.product',
        related='company_id.other_product_id',
        readonly=False
    )


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

