# -*- coding: utf-8 -*-
{
    'name': 'OLIB EMPLOYEE DETAILS',
    'summary': """This module will add a record to store employee details""",
    'version': '11.0.0.0.0',
    'description': """This module will add a record to store employee details""",
    'author': 'Daniel Abaka',
    'company': 'Orange Liberia',
    'website': 'http://www.orange.com',
    'category': 'Tools',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [

        'security/group.xml', 
        'views/employee_details_views.xml',
        'views/employee_configuration_views.xml',
        'security/ir.model.access.csv'


    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
