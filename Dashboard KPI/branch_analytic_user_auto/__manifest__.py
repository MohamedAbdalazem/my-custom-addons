# -*- coding: utf-8 -*-
{
    'name': 'Branch Analytic Account Auto Fill',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Automatically fill Analytic Account based on user branch',
    'description': "Automatically fills Analytic Account on Sales Orders, Invoices, and Payments based on the branch of the user.",
    'author': 'Custom',
    'depends': ['base','account','branch_analytic_journal','sale'],
    'data': [
        #'views/res_users_view.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml'
    ],
   'assets': {
       'web.assets_backend': [
            'branch_analytic_user_auto/static/src/js/disable_clipboard.js',
      ],
   },

    'installable': True,
    'application': False,
}
