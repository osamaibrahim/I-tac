from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class ResUserInherit(models.Model):
    _inherit = "res.users"
    sales_person_abbreviation = fields.Char(
        'Sales Person Abbreviation',
    )