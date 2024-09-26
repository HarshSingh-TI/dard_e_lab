{
    'name': 'Dard E Lab',
    'version': '1.0',
    'category': 'Pathology Management',
    'summary': 'Manage lab tests, blood reports and customer',
    'description': """This module provides features for managing pathology, including tests, customer details""",
    'depends': ['base','sale','product'],
    'data':[
        'security/ir.model.access.csv',
        "data/sequence.xml",
        'views/sale_order_confirmation_wizard_views.xml',
        'views/sale_order_inherit_views.xml',
        'views/worker_views.xml',
        'views/res_config_views.xml',
        'views/test_package_views.xml',
        'views/menu_views.xml',
        'report/custom_report_templates.xml',
        'report/worker_header_footer.xml',
        'report/report_template.xml',
        'report/worker_report_template.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}