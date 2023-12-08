# # -*- coding: utf-8 -*-
#
from odoo import models, fields, api


class AccountWizard(models.TransientModel):
    _name = "account.wizard"

    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    debit_account_shipping_id = fields.Many2one(comodel_name="account.account", string="Debit Account Shipping")
    credit_account_shipping_id = fields.Many2one(comodel_name="account.account", string="Credit Account Shipping")
    debit_account_other_id = fields.Many2one(comodel_name="account.account", string="Debit Account Other")
    credit_account_other_id = fields.Many2one(comodel_name="account.account", string="Credit Account Other")
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
    )

    def action_save(self):
        if self.debit_account_shipping_id:
            self.company_id.debit_account_shipping_id = self.debit_account_shipping_id.id
        if self.credit_account_shipping_id:
            self.company_id.credit_account_shipping_id = self.credit_account_shipping_id.id
        if self.debit_account_other_id:
            self.company_id.debit_account_other_id = self.debit_account_other_id.id
        if self.credit_account_other_id:
            self.company_id.credit_account_other_id = self.credit_account_other_id.id
        if self.journal_id:
            self.company_id.journal_id = self.journal_id.id

    @api.onchange('company_id')
    def company_save(self):
        if self.company_id.debit_account_shipping_id:
            self.debit_account_shipping_id = self.company_id.debit_account_shipping_id.id
        if self.company_id.credit_account_shipping_id:
            self.credit_account_shipping_id = self.company_id.credit_account_shipping_id.id
        if self.company_id.debit_account_other_id:
            self.debit_account_other_id = self.company_id.debit_account_other_id.id
        if self.company_id.credit_account_other_id:
            self.credit_account_other_id = self.company_id.credit_account_other_id.id
        if self.company_id.journal_id:
            self.journal_id = self.company_id.journal_id.id


class ResCompany(models.Model):
    _inherit = 'res.company'

    debit_account_shipping_id = fields.Many2one(comodel_name="account.account", string="Debit Account Shipping")
    credit_account_shipping_id = fields.Many2one(comodel_name="account.account", string="Credit Account Shipping")
    debit_account_other_id = fields.Many2one(comodel_name="account.account", string="Debit Account Other")
    credit_account_other_id = fields.Many2one(comodel_name="account.account", string="Credit Account Other")
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
    )
