# -*- coding: utf-8 -*-
{
    'name': 'OLIB LEAVE MODULE',
    'summary': """This module will make an employee to be able to request for leave""",
    'version': '11.0.0.0.0',
    'description': """This module will make an employee to be able to request for leave""",
    'author': 'Daniel Abaka',
    'company': 'Orange Liberia',
    'website': 'http://www.orange.com',
    'category': 'Tools',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'views/leave_request_views.xml',
        'views/leave_configuration_views.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
