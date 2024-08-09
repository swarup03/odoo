from odoo import fields, models,api,_
from odoo.exceptions import UserError


class CommissionOrder(models.Model):
    _name = "commission.order"
    _description = "This is order commission page."

    commission_find_id = fields.Many2one("commission.order.find", string="Commission Find")
    order_id = fields.Char(string='Order Reference', readonly=True)
    customer_name = fields.Char(string="Sales person", required=True)
    order_date = fields.Date(string="Order Date")
    commission = fields.Float(string="Commission")
    total = fields.Float(string="Total")
