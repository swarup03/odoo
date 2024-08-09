from odoo import http
from odoo.http import request
import json
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal as pager



class myMain(http.Controller):

    @http.route('/myhome', type='http', auth='public', website=True)
    def hello(self,**kwargs):
        # sale_orders = request.env['sale.order'].sudo().search([])
        sale_order_line = None
        view_table = False
        error = False
        if kwargs.get('search_order'):
            # sale_order_line = request.env['sale.order'].browse(int(orderNames))
            sale_order_line = request.env['sale.order'].search([('name', 'ilike', kwargs.get('search_order'))])
            if len(sale_order_line.ids) == 0:
                error = True
            view_table = True
        return request.render("website_custom.my_model_layout", {
            # 'sale_orders': sale_orders,
            'sale_order_line': sale_order_line,
            'view_table': view_table,
            'error': error,
        })

    @http.route('/myhome/submited', type='http', auth='public', methods=['GET', 'POST'], website=True)
    def status(self, **kwargs):
        if request.httprequest.method == 'POST':
            try:
                if request.env.user.name == "Public user":
                    request.env['public.data'].create({
                        'email': kwargs.get('email'),
                        'password': kwargs.get('password'),
                    })
                else:
                    request.env['signed.data'].create({
                        'user_id': request.env.uid,
                        'email': kwargs.get('email'),
                        'password': kwargs.get('password'),
                    })
                return request.redirect('/myhome/submited?status=success')
            except Exception as e:
                return request.redirect('/myhome/submited?status=error')

        elif request.httprequest.method == 'GET':
            status = kwargs.get('status')
            if status == "success":
                return request.render("website_custom.my_model_status")
            elif status == "error":
                return request.render("website_custom.my_model_status")
            else:
                return request.redirect('/myhome')

    @http.route('/saleOrder', type='http', auth='user', website=True)
    def saleOrders(self, **kwargs):
        order_data = request.env['sale.order'].search([('create_uid','=',request.env.uid),('access_token','!=',False)])
        print(order_data)
        return request.render("website_custom.shopping_customer_id", {
            'orders': order_data
        })
    
    @http.route('/saleOrder/<model("sale.order"):order>', type='http', auth='user', website=True)
    def saleOrder(self, order, access_token=None, **kwargs):
        if order.create_uid.id == request.env.uid:
            if order.access_token ==access_token:
                return request.render("website_custom.order_details", {
                    'order': order
                })
            else:
                return request.redirect('/saleOrder')
        else:
            return request.redirect('/saleOrder')
    
    @http.route('/myhome/sale_data', type='json', auth='public')
    def sold_total(self, **kwargs):
        sale_orders = request.env['sale.order'].sudo().search([('access_token','!=',False)])
        orders_data = [{'id':order.id,"name": order.name,'access_token': order.access_token} for order in sale_orders]
        return orders_data
    
    @http.route('/myhome/sale_data_form', type='json', auth='public')
    def sale_data(self, **kwargs):
        sale_orders = request.env['sale.order'].sudo().search([])
        orders_data = [{"id": order.id, "name": order.name, "access_token": order.access_token} for order in sale_orders]
        return orders_data
    
    @http.route('/myhome/sale_selected_data_form', type='json', auth='public')
    def sale_selected_data(self, **kwargs):
        sale_order = request.env['sale.order'].sudo().search([('id', '=', int(kwargs.get('id')))])
        orders_data = []

        for order in sale_order:
            order_data = {
                "id": order.id,
                "name": order.name,
                "access_token": order.access_token,
                "partner": order.partner_id.name,
                "order_date": order.date_order,
                "total_amount": order.currency_id.symbol + str(order.amount_total),
                "items": []
            }

            for line in order.order_line:
                product_image_url = f'/web/image/product.product/{line.product_id.id}/image_128'
                order_data["items"].append({
                    "product_name": line.product_id.name,
                    "quantity": line.product_uom_qty,
                    "price_subtotal": line.currency_id.symbol + str(line.price_subtotal),
                    "product_image": product_image_url
                })

            orders_data.append(order_data)

        return orders_data
        # <div class="alert alert-light text-dark border rounded-4" role="alert">

    @http.route('/myhome/sale_data_create', type='json', auth='public')
    def sale_data(self, **kwargs):
        if kwargs.get('id',"") != "":
            created_order = request.env['sale.order'].create({
                'partner_id': kwargs.get('id'),
                'partner_invoice_id': kwargs.get('id'),
                'partner_shipping_id': kwargs.get('id'),
                'user_id': request.env.uid,
            })
            created_order.action_confirm()
            return {'status': 'success'}

        partner_data = request.env['res.partner'].sudo().search([])
        partners = [{"id": order.id, "name": order.name} for order in partner_data]
        return partners

    @http.route('/get_categories', type='json', auth='public', methods=['POST'])
    def get_categories(self, query):
        categories = request.env['product.public.category'].search(['|',('name', 'ilike', query),('parent_id.name', 'ilike', query)])
        return [{'id': cat.id, 'name': cat.name} for cat in categories]
    