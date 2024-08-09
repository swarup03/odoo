from odoo import api, fields, models

class BookOrderLine(models.Model):
    """ For managing order lines of booked order """
    _name = "school.order.line"
    _description = "Lines of school Booked Order"
    _rec_name = "product_id"

    company_id = fields.Many2one('res.company', string='Company',
                                 help="Company of the booked order",
                                 default=lambda self: self.env.user.company_id)
    product_id = fields.Many2one('product.product',
                                 help="Select products for ordering",
                                 string='Product',
                                 domain=[('sale_ok', '=', True)],
                                 required=True, change_default=True)
    price_unit = fields.Float(string='Unit Price',
                              help="Unite price of selected product", digits=0)
    qty = fields.Float(string='Quantity', default=1,
                       help="Enter how much quantity of product want ")
    price_subtotal = fields.Float(compute='_compute_amount_line_all',
                                  digits=0,
                                  help="Sub total amount of each order line"
                                       "without tax",
                                  string='Subtotal w/o Tax')
    tax_ids = fields.Many2many('account.tax', string='Taxes',
                               readonly=True, help="Taxes for each line", default=lambda self: self.env['account.tax'].search([('amount', '=', 15)], limit=1))
    total_price = fields.Float(string="Total Amount",compute='_compute_amount_subtotal')
    discount = fields.Float(string='Discount (%)', digits=0, default=0.0,
                            help="You can apply discount for each product")
    order_id = fields.Many2one('school.order', string='Order Ref',
                               help="Relation to book order field",
                               ondelete='cascade')
    
    @api.depends('price_unit', 'qty', 'discount')
    def _compute_amount_line_all(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.order_id.company_id.currency_id, line.qty)
            line.price_subtotal = taxes['total_excluded']

    @api.depends('price_subtotal', 'tax_ids')
    def _compute_amount_subtotal(self):
        for line in self:
            taxes = line.tax_ids.compute_all(line.price_subtotal, line.order_id.company_id.currency_id, 1)
            line.total_price = taxes['total_included']

    @api.onchange('product_id')
    def _inchange_unit_price(self):
        self.price_unit = self.product_id.product_tmpl_id.list_price

