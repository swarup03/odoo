from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StoreTransferLine(models.Model):
    _name = 'store.transfer.line'
    _description = 'Store Transfer Line'

    transfer_id = fields.Many2one('store.transfer', string='Store Transfer', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)

    @api.constrains('quantity')
    def _check_quantity(self):
        for qty in self:
            if qty.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.transfer_id.state == 'confirmed':
                move_line = [(0, 0, {
                    'product_id': record.product_id.id,
                    'product_uom_qty': record.quantity,
                    'location_id': record.transfer_id.source_warehouse_id.lot_stock_id.id,
                    'location_dest_id': record.transfer_id.destination_warehouse_id.lot_stock_id.id,
                    'name': record.product_id.name,
                })]
                record.transfer_id.create_picking('', move_line)
            elif record.transfer_id.state == 'cancel' or record.transfer_id.state == 'done':
                raise ValidationError("Cannot add lines to a canceled transfer.")
        return records

    def write(self, vals):
        for record in self:
            if record.transfer_id.state == 'confirmed':
                if 'quantity' in vals:
                    for rec in record.transfer_id.picking_ids:
                        for prod in rec.move_ids_without_package:
                            if prod.product_id.id == record.product_id.id:
                                prod.product_uom_qty = vals['quantity']
                if 'product_id' in vals:
                    new_product_id = vals['product_id']
                    for rec in record.transfer_id.picking_ids:
                        for prod in rec.move_ids_without_package:
                            if prod.product_id.id == record.product_id.id:
                                prod.product_id = new_product_id
            elif record.transfer_id.state in ['done', 'cancel']:
                raise ValidationError("You cannot change the product information because the transfer state is in " + record.transfer_id.state + " state.")
        return super().write(vals)
        