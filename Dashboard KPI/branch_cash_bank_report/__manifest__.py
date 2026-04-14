{
    'name': 'تقرير الكاش والبنك لكل فرع',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'يعرض الكاش والبنك لكل فرع مع الحساب الرئيسي للشركة',
    'author': 'محمد عبدالعظيم',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/branch_cash_bank_report_view.xml',
    ],
    'installable': True,
    'application': False,
}
