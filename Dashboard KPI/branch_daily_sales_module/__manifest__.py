{
    'name': 'تقرير المبيعات اليومي لكل فرع',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'تقرير المبيعات اليومي لكل فرع باستخدام الحسابات التحليلية',
    'author': 'محمد عبدالعظيم',
    'depends': ['sale'],
    'data': [
        'views/branch_daily_sales_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}