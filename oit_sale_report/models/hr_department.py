from odoo import _, api, fields, models


class HrDepartment(models.Model):
    _inherit = "hr.department"
    department_abbreviation = fields.Char(
        'Department Abbreviation',
    )

