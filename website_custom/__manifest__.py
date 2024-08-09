{
    'name': 'Website Custom',
    'version': '17.0.0.1',
    'authors': 'swarup shah',
    'summary': 'Website Custom',
    'description': 'Website Custom',
    'sequence': -1,
    'category': 'website',
    'depends': ['base','website_sale','sale','school'],
    'data': [
        # 'data/payment_add.xml',
        'security/ir.model.access.csv',

        'views/menu.xml',
        'views/public_data_form.xml',
        'views/signed_data_form.xml',
        'views/website_menu.xml',
        'views/view_template.xml',
        'views/sale_view.xml',
        'views/order_detail.xml',
        'views/snippet_add.xml',
        'views/snippet_success.xml',
        'views/snippet_sale_order_name.xml',
        'views/snippet_sale_order_form.xml',
        'views/portal_create_sale_order.xml',
        'views/portel_add_section.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            'website_custom/static/src/views/js/validation.js',
            'website_custom/static/src/views/js/snippet_data_sale.js',
            'website_custom/static/src/views/js/snippet_data_sale_form.js',
            'website_custom/static/src/views/js/poteal_create_sale_order.js',
            'website_custom/static/src/views/js/search_category.js',
        ],
    }

}