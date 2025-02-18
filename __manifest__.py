{
    'name': 'IP VISITOR TRACKING',
    'version': '1.0',
    'summary': 'Integración con la API de IPGeolocation',
    'description': 'Obtención de geolocalización en tiempo real.',
    'author': 'Francisco Jiménez',
    'category': 'Website',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ip_visitor_tracking_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'icon': ['/ip_visitor_tracking/static/description/icon58.png'],
}