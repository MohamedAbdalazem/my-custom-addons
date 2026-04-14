{
    'name': 'Account Reconciliation (Community) with Partial Reconcile',
    'version': '1.2',
    'summary': 'Enable manual + partial reconciliation in Odoo 19 Community',
    'description': 'Adds Reconcile and Partial Reconcile (write-off wizard) for bank and cash accounts in Odoo Community Edition.',
    'category': 'Accounting',
    'author': 'Mohamed Abdalazem & ChatGPT',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'views/account_move_line_views.xml',
        'views/partial_reconcile_wizard_views.xml',
        'views/actions_menus.xml',
    ],
    'installable': True,
    'application': False,
}
