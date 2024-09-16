{
    'name': 'Dard E Lab',
    'version': '1.0',
    'category': 'Pathology Management',
    'summary': 'Manage lab tests, blood reports and customer',
    'description': """This module provides features for managing pathology, including tests, customer details""",
    'depends': ['base','sale','product'],
    'data':[
        # 'security/ir.model.access.csv',
        "data/sequence.xml",
        'views/sale_order_inherit_views.xml',
        'views/worker_views.xml',
        'views/test_package_views.xml',
        'views/menu_views.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}