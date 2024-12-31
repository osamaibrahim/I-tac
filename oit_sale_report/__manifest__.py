
{
    'name': 'OIT Sale Report',
    'summary': 'OIT Sale Report',
    'author': "Tarek Alhawy/OIT Solutions",
    'company': 'OIT Solutions',
    'website': "http://www.oit-solution.com",
    'version': '18.0',
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
        # security
        # 'security/ir.model.access.csv',
        # views
        # 'views/res_config_settings_views.xml',
        # 'views/sale_order.xml',
        # 'views/res_user.xml',
        # 'views/product_template.xml',
        # 'views/hr_department.xml',
        # reports
        # 'reports/sale_quote_report.xml',
        # 'reports/layouts.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

