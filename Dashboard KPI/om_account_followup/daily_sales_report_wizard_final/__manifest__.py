{
    'name': "Daily Sales Report Final Fixed",
    'version': '1.3',
    'summary': 'Daily sales report per branch (Analytic Account)',
    'description': "Generates daily sales report per branch, shows invoices per day, total, paid, balance, payment method, CSV export.",
    'author': 'Assistant',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/daily_sales_report_views.xml',
    ],
    'installable': True,
    'application': False,
}
