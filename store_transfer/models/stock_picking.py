from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    transfer_id = fields.Many2one("store.transfer", string="Stock Transfer")
    
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.transfer_id:
            self.transfer_id.state = 'done'
            if self.transfer_id.sale_order_id:
                sale_order = self.transfer_id.sale_order_id
                print(sale_order.id)
                if sale_order:
                    print(sale_order)
                    sale_order.state = 'draft'

                    context = {'order_id': sale_order.id}
                    sale_order.with_context(context).action_confirm()
                else:
                    raise UserError("Sale order not found!")
        return res

            
    
