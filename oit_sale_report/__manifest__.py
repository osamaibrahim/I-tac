
{
    'name': 'OIT Sale Report',
    'summary': 'OIT Sale Report',
    'author': "OIT Solutions",
    'company': 'OIT Solutions',
    'website': "http://www.oit-solution.com",
    'version': '15.0.0.1.0',
    'category': "OIT Solutions/apps",
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'sale',
        'hr',
        'account',
        'sale_management',
        'oit_sale_customize',
        'sale_order_line_product_image',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
'reports/sale_quote_report.xml',
'reports/layouts.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
        'views/hr_department.xml',

        'reports/sale_quote_report.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

