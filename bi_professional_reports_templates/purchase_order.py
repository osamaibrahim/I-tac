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
    shipping = fields.Float('Shipping')
    other = fields.Float()
    final_total = fields.Float('Total After shipping and Other', compute='compute_final_total')
    debit_account_shipping_id = fields.Many2one(
        'account.account', 'Debit Account',
        track_visibility='always',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.company.debit_account_shipping_id.id
    )
    credit_account_shipping_id = fields.Many2one(
        'account.account', 'Debit Account',
        track_visibility='always',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.company.credit_account_shipping_id.id
    )
    debit_account_other_id = fields.Many2one(
        'account.account', 'Debit Account',
        track_visibility='always',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.company.debit_account_shipping_id.id
    )
    credit_account_other_id = fields.Many2one(
        'account.account', 'Debit Account',
        track_visibility='always',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.company.credit_account_other_id.id
    )
    journal_id = fields.Many2one(
        'account.journal', 'journal',
        track_visibility='always',
        readonly=False,
        domain="[('type', '=', 'purchase')]",
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.company.journal_id.id
    )

    @api.depends('shipping', 'other', 'amount_total')
    def compute_final_total(self):
        for rec in self:
            rec.final_total = rec.shipping + rec.other + rec.amount_total

    def action_confirm_for_entry(self):
        account_move_obj = self.env['account.move']
        for rec in self:
            vals = []
            ref = rec.name
            if rec.shipping:
                vals.append((0, 0, {
                    'name': ref,
                    'account_id': rec.debit_account_shipping_id.id,
                    'partner_id': rec.partner_id.id,
                    'debit': rec.shipping,
                    'credit': 0.0
                }))
                vals.append((0, 0, {
                    'name': ref,
                    'account_id': rec.credit_account_shipping_id.id,
                    'partner_id': rec.partner_id.id,
                    'debit': 0.0,
                    'credit': rec.shipping
                }))
                if rec.other:
                    vals.append((0, 0, {
                        'name': ref,
                        'account_id': rec.debit_account_other_id.id,
                        'partner_id': rec.partner_id.id,
                        'debit': rec.other,
                        'credit': 0.0
                    }))
                    vals.append((0, 0, {
                        'name': ref,
                        'account_id': rec.credit_account_other_id.id,
                        'partner_id': rec.partner_id.id,
                        'debit': 0.0,
                        'credit': rec.other
                    }))

                move = account_move_obj.create(
                    {
                        'date': fields.Date.today(),
                        'ref': ref,
                        'journal_id': rec.journal_id.id,
                        'move_type': 'entry',
                        'line_ids': vals
                    })
                move.sudo().action_post()

    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        self.action_confirm_for_entry()
        return res
