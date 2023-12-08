{
    'name': 'Oit Report Invoice',
    'summary': 'Modifications on Invoice',
    'author': "OIT Solutions",
    'company': 'OIT Solutions',
    'website': "http://www.oit-solution.com",
    'version': '15.0.0.1.0',
    'category': "OIT Solutions/apps",
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'account',
        'l10n_gcc_invoice',
        'l10n_sa_invoice',
        'oit_sale_report',
        'bi_professional_reports_templates'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/res_company.xml',
        'views/account_move.xml',
        'report/arabic_english_invoice.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
