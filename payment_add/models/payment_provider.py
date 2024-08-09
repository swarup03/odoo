# -*- coding: utf-8 -*-

from odoo import _, api, models, fields
import hashlib,json,base64
import hmac
import time
import requests
from odoo.exceptions import UserError
import datetime


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'


    code = fields.Selection(
        selection_add=[('cybersource', "Cybersource")], ondelete={'cybersource': 'set default'})
    cybersource_merchant_id = fields.Char(string="merchant Id", required_if_provider='stripe', groups='base.group_system')
    cybersource_api_key_id = fields.Char(string="Api key", required_if_provider='stripe', groups='base.group_system')
    cybersource_secret_key = fields.Char(string="Secret Key", required_if_provider='stripe', groups='base.group_system')

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'cybersource').update({
            'support_express_checkout': True,
            'support_manual_capture': 'full_only',
            'support_refund': 'partial',
            'support_tokenization': True,
        })

class saleOrder(models.Model):
    _inherit = "sale.order"

    def pay_now(self):
        payload= {
            "clientReferenceInformation": {
                "code": "TC50171_3"
            },
            "paymentInformation": {
                "card": {
                "number": "4111111111111111",
                "expirationMonth": "12",
                "expirationYear": "2031"
                }
            },
            "orderInformation": {
                "amountDetails": {
                "totalAmount": "102.21",
                "currency": "USD"
                },
                "billTo": {
                "firstName": "John",
                "lastName": "Doe",
                "address1": "1 Market St",
                "locality": "san francisco",
                "administrativeArea": "CA",
                "postalCode": "94105",
                "country": "US",
                "email": "test@cybs.com",
                "phoneNumber": "4158880000"
                }
            }
        }
        hashobj = hashlib.sha256()
        hashobj.update(json.dumps(payload).encode('utf-8'))
        hash_data = hashobj.digest()
        digest = base64.b64encode(hash_data)
        print(digest)
        payload = {
            "host": "apitest.cybersource.com",
            "date": "Wed, 10 Jul 2024 13:09:39 GMT",
            "(request-target)": "post /pts/v2/payments",
            "digest": digest,
            "v-c-merchant-id": "swarup2003_1720528036"
        }
        secret_key = "sBgsdhcRlukmW55uzMJOc8GzxFbbkjGqV4x2jYWPUBA="

        headers = ["host", "date", "(request-target)", "digest", "v-c-merchant-id"]
        signature_string = "\n".join(f"{header}: {payload[header]}" for header in headers)

        # Generate the HMAC-SHA256 hash
        signature = hmac.new(secret_key.encode("utf-8"), signature_string.encode("utf-8"), hashlib.sha256)
        base64_signature = base64.b64encode(signature.digest()).decode("utf-8")

        print(base64_signature)


    def get_digest(self, payload):
        hashobj = hashlib.sha256()
        hashobj.update(json.dumps(payload).encode('utf-8'))
        hash_data = hashobj.digest()
        digest = base64.b64encode(hash_data)
        return digest.decode('utf-8')

    def get_signature(self, method, resource, timestamp, digest, secret_key, key_id,merchant_id):
        merchant_id = 'swarup2003_1720528036'
        signature_header = f"host: apitest.cybersource.com\nv-c-date: {timestamp}\nrequest-target: {method} {resource}\ndigest: SHA-256={digest}\nv-c-merchant-id: {merchant_id}"
        signature = base64.b64encode(
            hmac.new(base64.b64decode(secret_key), signature_header.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        signature = f'keyid="{key_id}", algorithm="HmacSHA256", headers="host v-c-date request-target digest v-c-merchant-id", signature="{signature}"'
        return signature

    def action_capture_in_cybersource(self):
        self.ensure_one()

        payment_prov_data = self.env["payment.provider"].search([('code','=','cybersource')])
        merchant_id = ''
        key_id = ''
        secret_key = ""
        for prov in payment_prov_data:
            # print("<<<<<<<<<<<<",prov)
            merchant_id = prov.cybersource_merchant_id
            key_id = prov.cybersource_api_key_id
            secret_key = prov.cybersource_secret_key
        if not self.partner_id.email:
            raise UserError('Customer email is required to process the payment.')

        cybersource_url = 'https://apitest.cybersource.com/pts/v2/payments'
        print(self.country_code)
        # print(self.partner_id.)
        payment_data = {
            "clientReferenceInformation": {
                "code": self.name
            },
            "paymentInformation": {
                "card": {
                "number": "4111111111111111",
                "expirationMonth": "12",
                "expirationYear": "2031"
                }
            },
            "orderInformation": {
                "amountDetails": {
                    "totalAmount": self.amount_total,
                    "currency": self.currency_id.name
                },
                "billTo": {
                    "firstName": self.partner_id.name.split()[0],
                    "lastName": self.partner_id.name.split()[-1],
                    "address1": self.partner_id.street,
                    "locality": self.partner_id.city,
                    "administrativeArea": self.partner_id.state_id.code,
                    "postalCode": self.partner_id.zip,
                    "country": self.partner_id.country_id.code,
                    "email": self.partner_id.email,
                    "phoneNumber": self.partner_id.phone
                },
            }
        }
        # print(payment_data)

        timestamp = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        digest = self.get_digest(payment_data)
        signature = self.get_signature("post", "/pts/v2/payments", timestamp, digest, secret_key, key_id, merchant_id)

        headers = {
            'host': "apitest.cybersource.com",
            'v-c-date': timestamp,
            'digest': f"SHA-256={digest}",
            'v-c-merchant-id': merchant_id,
            'signature': signature,
            'Content-Type': 'application/json'
        }

        response = requests.post(cybersource_url, headers=headers, data=json.dumps(payment_data))
        print(response)
        
        if response.status_code == 201:
            self.message_post(body="Payment successfully captured via CyberSource.")
            self._create_invoices()
        else:
            self.message_post(body=f"Failed to capture payment: {response.text}")
    
    def test_paym(self):
        print(self)
        # x = self._send_payment_succeeded_for_order_mail()
        # x = self.payment_action_capture()
        # x = self.payment_action_void()
        x = self.env['payment.transaction']._set_pending()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",x)