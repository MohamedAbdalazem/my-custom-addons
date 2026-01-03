{
    'name': 'POS Prevent Negative Quantity',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'منع بيع المنتجات غير المتوفرة مع تنبيه عربي',
    'depends': ['point_of_sale', 'stock'],
    'assets': {
        'point_of_sale.assets': [
            'pos_prevent_negative_qty/static/src/js/prevent_negative_qty.js',
        ],
    },
    'installable': True,
    'application': False,
}
