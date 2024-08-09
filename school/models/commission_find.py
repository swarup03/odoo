from odoo import fields, models, api, _

class CommissionOrder(models.Model):
    _name = "commission.order.find"
    _description = "This is order commission page."

    customer_name = fields.Many2one("res.users", string="Customer Name", required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    order_ids = fields.One2many("commission.order", "commission_find_id", string="Orders")
    total_tax = fields.Float("Total Commission", compute="_compute_total_amount")
    total_amount = fields.Float("Total Amount",compute="_compute_total_amount")
            
            
    @api.depends('order_ids.commission', 'order_ids.total')
    def _compute_total_amount(self):
        for record in self:
            # record.total_tax = sum(order.commission for order in record.order_ids)
            record.total_amount = sum(order.total for order in record.order_ids)
            # if record.total_amount > record.partner_id.commission_amount_on:
            #     record.total_tax = (record.total_amount*record.partner_id.percentage)/100
            # else:
            record.total_tax = sum(order.commission for order in record.order_ids)
            
    def search_order_list(self):
        print(self.customer_name.name)
        domain = [
            ('customer_name', '=', self.customer_name.name),
            ('order_date', '>=', self.start_date),
            ('order_date', '<=', self.end_date),
        ]
        orders = self.env['commission.order'].search(domain)
        print(orders)
        self.order_ids = [(6, 0, orders.ids)]
        