""" Initialize Res Company """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    header = fields.Binary(string="Company Header")
    footer = fields.Binary(string="Company Footer")


class BaseDocumentLayout(models.Model):
    _inherit = 'base.document.layout'

    header = fields.Binary(related="company_id.header")
    footer = fields.Binary(related="company_id.footer")
