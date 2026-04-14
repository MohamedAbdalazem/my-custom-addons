{
    'name': 'Account Reconciliation (Community)',
    'version': '1.0',
    'summary': 'Enable manual reconciliation feature in Odoo 19 Community',
    'description': 'Adds a Reconcile button and reconciliation options for bank and cash accounts in Odoo Community Edition.',
    'category': 'Accounting',
    'author': 'Mohamed Abdalazem & ChatGPT',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'views/account_move_line_views.xml',
    ],
    'installable': True,
    'application': False,
}
