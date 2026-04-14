{
    'name': "Daily Sales Report",
    'version': '1.0',
    'summary': 'Daily sales report per branch (Analytic Account)',
    'description': """Generates daily sales report per branch (Analytic Account).
Features:
- Shows invoices per day
- Filter by branch and date
- Shows Total, Paid, Balance
- Export to CSV/Excel
""",
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
