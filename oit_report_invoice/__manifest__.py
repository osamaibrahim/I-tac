{
    'name': 'Oit Report Invoice',

    'summary': 'Modifications on Invoice',

    'author': "Tarek Alhawy/OIT Solutions",

    'company': 'OIT Solutions',

    'website': "http://www.oit-solution.com",

    'version': '18.0',

    'category': "OIT Solutions/apps",

    'license': 'AGPL-3',

    'depends': ['account', 'l10n_gcc_invoice', 'l10n_sa', 'oit_sale_report'],
    'data': [
        # views
        'views/account_move.xml',
        'views/partner_view.xml',
        # report
        'report/arabic_english_invoice.xml',
    ],

    'assets': {
        'web.report_assets_common': [
            'oit_report_invoice/static/src/css/font.css',
        ]
    },

    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
