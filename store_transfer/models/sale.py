from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderSale(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('store_transfers', "Store Transfers"),
        ('cancel_store_transfers', "Cancel Store Transfers")],
    )
    destination_warehouse = fields.Many2one('stock.warehouse', string="Destination Warehouse", required=True)
    store_transfer_count = fields.Integer(string="Store Transfer", default=0)


    def action_confirm(self):
        for order in self:
            origin = self.env.context.get('order_id', '')
            if origin != "":
                print("breaking")
                break
            product_qty_needed = {}

            for line in order.order_line:
                product_qty_available = line.product_id.with_context(warehouse=order.warehouse_id.id).qty_available
                print("=====================", product_qty_available)

                if product_qty_available < line.product_uom_qty:
                    product_qty_needed[line.product_id] = line.product_uom_qty - product_qty_available
            print(product_qty_needed)
            if product_qty_needed != {}:
                print("========")
                # source_warehouse = self.env['stock.warehouse'].search([('code', '=', 'BVS')], limit=1)
                source_warehouse = self.env['stock.warehouse'].browse(self.destination_warehouse.id)

                if not source_warehouse:
                    raise UserError('Insufficient stock and no other warehouses available.')

                transfer_lines = [(0, 0, {
                    'product_id': product.id,
                    'quantity': qty_needed
                }) for product, qty_needed in product_qty_needed.items()]

                transfer = self.env['store.transfer'].create({
                    'source_warehouse_id': source_warehouse.id,
                    'destination_warehouse_id': order.warehouse_id.id,
                    'transfer_line_ids': transfer_lines,
                    'sale_order_id': order.id  # Link the transfer to the sale order
                })

                order.state = 'store_transfers'
                context = {'order_name': order.name}
                transfer.with_context(context).approve_transfer()
                self.store_transfer_count += 1
                return True  

        return super(SaleOrderSale, self).action_confirm()

    def action_view_shop(self):
        order = self.env['store.transfer'].search([('sale_order_id','=',self.id)])
        print(order)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('transfer_id', '=', order.id)],
            'context': {'create': False}
        }

