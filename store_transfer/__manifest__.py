{
    'name': 'Store Transfer',
    'version': '17.0.0.1',
    'authors': 'swarup shah',
    'summary': 'Implement Custom Object for Store Transfer',
    'description': 'Implement Custom Object for Store Transfer',
    'sequence': -1,
    # 'category': 'sale',
    'depends': ['base','sale','stock'],
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'data/add_warehouse.xml',
        'views/menu.xml',
        'views/store_transfer_view.xml',
        'views/sale_order_viwe.xml',
    ]
}