from odoo import http
from odoo.http import request
import json


class Main(http.Controller):

    @http.route('/create_sale_order', type='json', auth='users', methods=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        # Extract data from the request (this example assumes JSON payload)
        print(kwargs)
        order_data = json.loads(request.httprequest.data)
        print(kwargs)
        # print("<<<<<<<<<<<<<<<<",order_data)

        # Create a new sale order
        try:
            sale_order = request.env['sale.order'].sudo().create({
                'partner_id': order_data.get('partner_id'),
                'user_id': order_data.get('user_id'),
                'order_line': [(0, 0, {
                    'product_id': line['product_id'],
                    'product_uom_qty': line['quantity'],
                    'price_unit': request.env['product.product'].sudo().browse(line['product_id']).lst_price,
                }) for line in order_data.get('order_lines', [])]
            })

            return {'status': 'success', 'sale_order_id': sale_order.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/website/form/mail.mail', type='json', auth='public', methods=['POST'], website=True)
    def create_email(self, **kwargs):
        values = json.loads(request.httprequest.data)
        # print(values)
        val = values.get('data_value')
        if values:
            mail_mail = request.env['mail.mail'].sudo().create(val)
            if mail_mail:
                mail_mail.send()
            return {'status': 'success', 'message': 'Email created successfully'}
        return {'status': 'error', 'message': 'Missing values'}


    @http.route('/sale_order_form', type='http', auth='public', website=True)
    def show_sale_order_form(self, **kwargs):
        return request.render("school.sale_order_form")


    # @http.route('/shopping_mall/<name>', auth='public')
    # def show_name(self, name):
    #     return '<h1>{}</h1>'.format(name)


    # @http.route('/shopping_mall/veera_web', auth='public')
    # def veera(self, **kwargs):
    #     return request.render("shopping_mall.veera_custom_id", {})
