from odoo import api, fields, models

class SchoolOrder(models.Model):
    _name = 'school.order'
    _description = 'School Product Order'

    name = fields.Char(string='Booking Ref', readonly=True, copy=False, default='/')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id, readonly=True)
    date_order = fields.Date(string='Order Date', default=fields.Date.today(), readonly=True)
    amount_total = fields.Float(string='Total', digits=0, compute='_compute_amount_total', store=True)
    note = fields.Text(string='Note')
    delivery_address = fields.Char(string='Delivery Address')
    delivery_date = fields.Date(string='Delivery Date')
    school_id = fields.Many2one("school.profile", string="School")
    amount_tax = fields.Float(string='Taxes', compute='_compute_amount_tax', store=True, help="Tax amount for the order")
    order_line_ids = fields.One2many('school.order.line', 'order_id', string='Order Lines')

    @api.depends('order_line_ids.price_subtotal', 'order_line_ids.tax_ids')
    def _compute_amount_tax(self):
        for order in self:
            total_tax = 0.0
            for line in order.order_line_ids:
                taxes = line.tax_ids.compute_all(line.price_subtotal, order.company_id.currency_id, line.qty)
                total_tax += taxes['total_included'] - taxes['total_excluded']
            order.amount_tax = total_tax

    @api.depends('order_line_ids.total_price', 'amount_tax')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(line.total_price for line in order.order_line_ids) 

    @api.model
    def set_school_data(self, data):
        address_list = self.env['school.profile'].search_read([('id', '=', data.get('school_id'))], ['street', 'street2', 'country_id', 'state_id', 'city', 'zip'])
        address = ""
        for i in address_list:
            address += (i.get('street') + " ") if i.get('street') else ""
            address += (i.get('street2') + " ") if i.get('street2') else ""
            address += (i.get('city') + " ") if i.get('city') else ""
            address += (i.get('state_id')[1] + " ") if i.get('state_id') and i.get('state_id')[1] else ""
            address += (i.get('country_id')[1] + " ") if i.get('country_id') and i.get('country_id')[1] else ""
            address += (i.get('zip') + " ") if i.get('zip') else ""

        ord_id = self.create({
            'name': self.env['ir.sequence'].next_by_code('school.order'),
            'school_id': data.get('school_id'),
            'delivery_date': data.get('deliveryDate'),
            'note': data.get('note'),
            'delivery_address': address,
        })

        param_obj = self.env['ir.config_parameter'].sudo()
        discount_limit = 0
        if param_obj.get_param('sale_discount_limit.is_discount_limit'):
            discount_limit = param_obj.get_param('sale_discount_limit.discount_limit', default=0.0)

        for prod in data.get('productOrderLine'):
            self.env['school.order.line'].create({
                'product_id': prod.get('id'),
                'qty': prod.get('quantity'),
                'order_id': ord_id.id,
                'price_unit': self.env['product.product'].browse(prod.get('id')).lst_price,
                'discount': float(discount_limit),
            })

        ord_id._compute_amount_tax()
        ord_id._compute_amount_total()
