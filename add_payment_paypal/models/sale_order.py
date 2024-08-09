# -*- coding: utf-8 -*-

from odoo import _, models
from odoo import exceptions
import base64, requests

class saleOrder(models.Model):
    _inherit = "sale.order"

    def action_paypal_pay(self):
        if not self:
            raise exceptions.UserError("No record found to process.")
        client_id = 'AWx4wvfV1lz5huPtvzfyN2csL65ctFTwX5XVvcHuU-QwSmCjAwa1Spil1D4upj2E8YtHyNIT71BymZic'
        secret_id = 'EHXCOzNBW75_9olZ2d7VYvH9H6mRwXWhYmk4_OK5Hmw8f_jbLnojR_unc_j8bsbCyAyW3E3syt3dcHpP'
        api_url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'
        for order in self:
            access_token = base64.b64encode(f"{client_id}:{secret_id}".encode()).decode()
            print(">>>>>>>>>>>>>>>>>>>>",access_token)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {access_token}'
            }
            order_data = {
                'intent': 'CAPTURE',
                'purchase_units': [{
                    'amount': {
                        'currency_code': 'USD',
                        'value': str(order.amount_total)
                    },
                    'description': order.name
                }]
            }
            print("order data",order_data)
            response = requests.post(api_url, json=order_data, headers=headers)
            response.raise_for_status()
            print("====",response)
            return response.json()