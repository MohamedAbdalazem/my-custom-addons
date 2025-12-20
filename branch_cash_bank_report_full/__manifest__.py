{
    'name': 'تقرير الكاش والبنك لكل فرع - Branch Cash & Bank Report',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'يعرض كاش وبنك لكل فرع مع طباعة PDF (عربي / English)',
    'author': 'محمد عبدالعظيم',
    'depends': ['account', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/branch_cash_bank_view.xml',
        'views/branch_cash_bank_menu.xml',
        'reports/branch_cash_bank_template.xml',
    ],
    'installable': True,
    'application': False,
}
