""" Initialize Sale Report """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleOrderReportProforma(models.AbstractModel):
    _inherit = 'sale.report'
    _description = 'Proforma Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if self.state =='draft':
            raise ValidationError('You can not print on draft state !')

        docs = self.env['sale.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs,
            'proforma': True
        }
