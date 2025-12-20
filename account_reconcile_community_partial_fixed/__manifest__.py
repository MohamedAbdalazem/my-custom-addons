{
    'name': 'Account Reconcile Community Partial (Fixed)',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Add full and partial reconciliation for Odoo 19 Community',
    'depends': ['account'],
    'data': [
        'views/account_move_line_views.xml',
        'views/partial_reconcile_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}
