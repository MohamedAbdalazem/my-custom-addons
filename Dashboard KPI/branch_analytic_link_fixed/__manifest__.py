{
    'name': 'Branch Analytic Link',
    'version': '2.2',
    'category': 'Accounting',
    'summary': 'Auto link branch, analytic account, and generate daily branch report with Excel & PDF',
    'author': 'Custom by Mohamed & GPT Assistant',
    'depends': ['account', 'analytic', 'sale_management', 'point_of_sale'],
    'data': [
        'report/branch_daily_report.xml',
        'report/branch_daily_report_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}