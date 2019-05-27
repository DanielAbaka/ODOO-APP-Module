# -*- coding: utf-8 -*-
{
    'name': 'VEHICLE REQUEST MODULE',
    'summary': "This module will allow an employee to make several request...",
    'version': '11.0.0.0.1',
    'author': 'Daniel Abaka',
    'company': 'Orange Liberia',
    'website': 'http://www.orange.com',
    'category': 'Tools',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [  
        'security/group.xml',  
        'views/vehicle_request_view.xml',
        'views/service_request_view.xml',
        'views/security_check_view.xml',
        # 'views/product_request.xml',
        'views/vehicle_total_request_view.xml',
        'views/security_check_total_view.xml',
        'views/vehicle_service_total_request_view.xml',
        'views/vehicle_request_report_view.xml',
        'views/leave_request_report_view.xml',
        'views/security_check_report_view.xml',
        'views/vehicle_service_request_report_view.xml',
        'security/ir.model.access.csv'
        
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
