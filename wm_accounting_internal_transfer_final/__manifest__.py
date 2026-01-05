# -*- coding: utf-8 -*-
{
    'name': 'wm_accounting_internal_transfer_final',
    'version': '1.2',
    'category': 'Accounting',
    'summary': 'Internal Bank/Cash Transfers with Arabic Interface',
    'depends': ['account', 'base_accounting_kit'],
    'data': [
        'views/account_payment_view.xml',
        'wizard/internal_transfer_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
}
