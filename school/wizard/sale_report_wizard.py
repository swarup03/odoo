from odoo import fields, models, api, _


class saleReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'
    _description = "This is a sale report wizard."

    order_id = fields.Many2one('sale.order', string="Orders")
    order_line_ids = fields.Many2many(
        'sale.order.line', string="Orders Line")

    
    def confirm_generate_report(self):
        report_data = {
            'order_id': self.order_id.id,
            'order_line_ids': [(6, 0, self.order_line_ids.ids)]
        }
        return self.env.ref('Online_shopping_report_saleorder_document').report_action(self, data=report_data)
    
    def print_report(self):
        # print(" order _idf >>>>>>>>>>>", self.order_id)
        print(">>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>",self.env.context.get('active_id'))
        print(" selected order line <<<<<<<<<<<<<", self.order_line_ids)
        order_line = self.order_line_ids.mapped('id')
        print(" selected order line <<<<<<<<<<<<<", order_line)
        action = self.env.ref('school.action_sale_order_template').with_context(my_report = True, order_lines = order_line).report_action(self.order_id)
        print(action)

        return action
    def print_inherit_report(self):
        print(" selected order line <<<<<<<<<<<<<", self.order_line_ids)
        order_line = self.order_line_ids.mapped('id')
        print(" selected order line <<<<<<<<<<<<<", order_line)
        action = self.env.ref('sale.action_report_saleorder').with_context(my_report = True, order_lines = order_line).report_action(self.order_id)
        print(action)
        return action

