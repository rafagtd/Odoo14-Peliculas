# -*- coding:utf-8 -*-
{
    'name': 'Modulo de peliculas',
    'version': '1.0',
    'depends': [
        'contacts', 'mail',
    ],
    'author': 'Rafa GtD',
    'category': 'Peliculas',
    'website': 'http://www.entretablas.com',
    'summary': 'Modulo de presupuestos para peliculas',
    'description': '''
    Modulo para hacer presupuestos de peliculas
    ''',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/categoria.xml',
        'data/secuencia.xml',
        'wizard/update_wizard_views.xml',
        'views/menu.xml',
        'views/presupuesto_view.xml',
    ]
}

