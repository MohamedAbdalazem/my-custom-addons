# -*- coding:utf-8 -*-
{
    'name': "Accounting Internal Transfer",
    'summary': """
        This module restores the internal payment transfer feature that was available in Odoo version 17 and earlier.
Internal Transfer
Bank Transfer
Cash Transfer
Bank Internal Transfer
Cash Internal Transfer
accounting internal transfer
account internal transfer
payment internal transfer
Odoo 17 internal transfer
odoo17 payment internal transfer
        """,
    'description': """
     This module restores the internal payment transfer feature that was available in Odoo version 17 and earlier.
    """,
    'category': 'Accounting',
    'version': '1.0.1',
    'license': 'OPL-1',
    'author': "Waleed Mohsen",
    'support': 'mohsen.waleed@gmail.com',
    'currency': 'USD',
    'price': 20.0,
    'depends': ['account'],
    'data': [
        'views/account_payment_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
}

