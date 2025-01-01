
{
    'name': 'OIT Report Layout',

    'summary': 'OIT Report Layout',

    'author': "Tarek Alhawy/OIT Solutions",

    'company': 'OIT Solutions',

    'website': "http://www.oit-solution.com",

    'version': '18.0',

    'category': "OIT Solutions/apps",

    'license': 'AGPL-3',

    'depends': ['base', 'web'],

    'data': [
        # views
        'views/res_company.xml',
        'views/report_layout.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}

