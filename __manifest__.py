{
    'name': 'IP Visitor Tracking',
    'version': '1.0',
    'summary': 'Módulo para rastrear la geolocalización de los visitantes del sitio web.',
    'description': 'Este módulo utiliza la API de ipgeolocation.io para obtener información de geolocalización de los visitantes.',
    'author': 'Francisco Jiménez',
    'category': 'Website',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/visitor_tracking_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'icon': '/ip_visitor_tracking/static/description/icon.png',
}