{
    'name': 'POS Noo Negative Stock',
    'version': '1.0',
    'author': 'Mohamed & ChatGPT',
    'depends': ['point_of_sale', 'stock'],
    'summary': 'منع البيع في نقاط البيع عند نفاد المخزون',
    'data': [],
    'assets': {
        'point_of_sale.assets': [
            '/pos_no_negative_stock_odoo19/static/src/js/pos_no_negative_stock.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
