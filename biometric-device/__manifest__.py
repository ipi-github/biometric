# -*- coding: utf-8 -*-
{
    'name': "McGeorge Consulting Biometric Device integrations",

    'summary': """
        Biometric Device integrations
        """,

    'description': """
        Biometric Device integrations
    """,

    'author': "McGeorge Consulting Ltd",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'portal', 'hr_attendance', ],

    # always loaded
    'data': [
        'data/data.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
