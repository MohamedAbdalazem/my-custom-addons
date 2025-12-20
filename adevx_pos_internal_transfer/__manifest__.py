{
    'name': "POS Internal Transfer",

    'summary': """POS Internal Transfer""",
    'description': """POS Internal Transfer""",

    'category': 'Sales/Point of Sale',
    'author': 'Adevx',
    'license': "OPL-1",
    'website': 'https://adevx.com',
    "price": 0,
    "currency": 'USD',

    'depends': ['point_of_sale', 'stock'],
    'data': [
        # Views
        'views/pos_config.xml'
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "adevx_pos_internal_transfer/static/src/**/*"
        ]
    },

    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
