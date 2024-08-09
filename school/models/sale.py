from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessError
from datetime import datetime, timedelta
import base64
import io
import xlsxwriter

class SaleOrder(models.Model):
    _inherit = "sale.order"

    checking_date = fields.Date(
        string="Ordering Date", help="enter the date when order was placed")

    nick_name = fields.Char(string="Nick Name")
    commission = fields.Float(
        string="Commission", compute="compute_commision_amount")

    state = fields.Selection(
        selection_add=[('to_approve', "To Approve")],
    )

    # @api.depends("amount_total")
    # def compute_commision_amount(self):
    #     for i in self:
    #         if i.total_amount > i.partner_id.commission_amount_on:
    #             i.commission = (i.total_amount*i.partner_id.percentage)/100
    #         else:
    #             i.commission = sum(order.commission for order in record.order_ids)

    commission_order_id = fields.Many2one(
        'commission.order', string='Commission Order', readonly=True)

    # def action_confirm(self):
    #     res = super(SaleOrder, self).action_confirm()
    #     commission_value =0.0
    #     if self.amount_total > self.user_id.partner_id.commission_amount_on:
    #         # print("partner_id.commission_amount_on",self.user_id.partner_id.commission_amount_on)
    #         commission_value = (self.amount_total*self.user_id.partner_id.percentage)/100
            
    #     if self.commission_order_id:
    #         self.commission_order_id.write({
    #             'order_id': self.name,
    #             'customer_name': self.user_id.name,
    #             'order_date': self.date_order,
    #             'commission': commission_value,
    #             'total': self.amount_total,
    #         })
    #     else:
    #         commission_order = self.env['commission.order'].create({
    #             'order_id': self.name,
    #             'customer_name': self.user_id.name,
    #             'order_date': self.date_order,
    #             'commission': commission_value,
    #             'total': self.amount_total,
    #         })
    #         self.commission_order_id = commission_order.id
        
    #     mail_template = self.env.ref('school.mail_order_comfirm_blog')
    #     mail_template.send_mail(self.id, force_send=True)
    #     return res

    # def action_cancel(self):
    #     res = super(SaleOrder, self).action_cancel()
    #     if self.commission_order_id:
    #         self.commission_order_id.unlink()
    #     return res


    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Call super to invoke the parent create method
    #     orders = super(SaleOrder, self).create(vals_list)
    #     print(orders.id)
    #     param_obj = self.env['ir.config_parameter'].sudo()
    #     amount_limit = param_obj.get_param('sale_discount_limit.amount_limit', default=0.0)
    #     print(amount_limit)
    #     print(orders.tax_totals.get('amount_total'))
    #     if float(amount_limit) < orders.tax_totals.get('amount_total'):
    #         orders.state = 'to_approve'

    #     return orders
    
    def action_confirm(self):
        param_obj = self.env['ir.config_parameter'].sudo()
        amount_limit = param_obj.get_param('sale_discount_limit.amount_limit', default=0.0)
        for order in self:
            if order.amount_total > float(amount_limit):
                order.state = "to_approve"
            else:
                super(SaleOrder, self).action_confirm()
        return True        

    def _get_order_lines_to_report(self):
        order_lines_context = self.env.context.get('order_lines')
        if order_lines_context:
            return self.order_line.filtered(lambda l: l.id in order_lines_context)
        return super(SaleOrder, self)._get_order_lines_to_report()

    def add_download_report_action(self):
        return {
            'name': 'Download Report',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }
    def action_xlsx_report_download(self, data_add, start_date, end_date,user_id):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Sales Report')

        # Define styles
        bold_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter', 
            'bg_color': '#FF5733', 'border': True, 'text_wrap': True
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 12, 'valign': 'vcenter', 
            'bg_color': '#FFEB3B', 'font_color': '#008000', 'border': True, 'text_wrap': True
        })
        normal_format = workbook.add_format({
            'text_wrap': True, 'align': 'left', 'valign': 'top', 'border': True
        })
        number_format = workbook.add_format({
            'text_wrap': True, 'align': 'right', 'border': True
        })
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yy', 'align': 'left', 'valign': 'top', 'border': True
        })
        total_format = workbook.add_format({
            'bold': True, 'bg_color': '#FFEB3B', 'border': True  # Yellow background for totals
        })

        # Set column sizes
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 7)
        sheet.set_column('C:D',13)
        sheet.set_column('E:F',15)
        sheet.set_column('G:G',10)
        sheet.set_column('H:H',25)
        sheet.set_column('I:L',12)
        sheet.set_column('O:O',10)
        sheet.set_column('P:P',10)
        sheet.set_default_row(20)  # Adjust the height as needed
        sheet.set_row(0, 30)

        # Write report header
        report_header = f"Sale report from {start_date} to {end_date}"
        sheet.merge_range('A1:P1', report_header, header_format)
        sheet.set_row(0, 25)  # Set row height for the header
        sheet.set_row(1, 30)

        # Write headers with bold format
        headers = [
            'S.No', 'Number', 'Order Date', 'Expected date', 'Customer', 'Salesperson', 'Sales Team', 'Company',
            'Untaxed amount', 'Taxes', 'Amount Total', 'Tags', 'Status', 'Delivery status', 'Invoice status',
            'Amount to invoice'
        ]
        for i, header in enumerate(headers):
            sheet.write(1, i, header, bold_format)

        data = data_add
        row = 2  # Start from the third row

        # Initialize column totals
        column_totals = [0] * 4  # Columns H, I, J,O

        currency_symbol = ''
        i=0
        for i,rec in enumerate(data,start=1):
            currency_symbol = rec.currency_id.symbol if rec.currency_id else ''
            sheet.write(row, 0, int(i), number_format)
            sheet.write(row, 1, (rec.name or '').capitalize(), normal_format)
            sheet.write(row, 2, rec.date_order.strftime('%d-%m-%y') if rec.date_order else 'Na', date_format)
            sheet.write(row, 3, rec.expected_date.strftime('%d-%m-%y') if rec.expected_date else 'Na', date_format)
            sheet.write(row, 4, (rec.partner_id.name or '').capitalize(), normal_format)
            sheet.write(row, 5, (rec.user_id.name or '').capitalize(), normal_format)
            sheet.write(row, 6, (rec.team_id.name or '').capitalize(), normal_format)
            sheet.write(row, 7, (rec.company_id.name or '').capitalize(), normal_format)
            sheet.write(row, 8, f"{currency_symbol}{round(rec.amount_untaxed,2) or '0.00'}", normal_format)
            sheet.write(row, 9, f"{currency_symbol}{round(rec.amount_tax,2) or '0.00'}", normal_format)
            sheet.write(row, 10, f"{currency_symbol}{round(rec.amount_total,2) or '0.00'}", normal_format)
            sheet.write(row, 11, ', '.join(tag.name.capitalize() for tag in rec.tag_ids) or 'NA', normal_format)
            sheet.write(row, 12, (rec.state or 'NA').capitalize(), normal_format)
            sheet.write(row, 13, (rec.delivery_status or 'NA').capitalize(), normal_format)
            sheet.write(row, 14, (rec.invoice_status or 'NA').capitalize(), normal_format)
            sheet.write(row, 15, f"{currency_symbol}{round(rec.amount_to_invoice,2) or '0.00'}", normal_format)

            # Update column totals
            column_totals[0] += rec.amount_untaxed or 0
            column_totals[1] += rec.amount_tax or 0
            column_totals[2] += rec.amount_total or 0
            column_totals[3] += rec.amount_to_invoice or 0

            # Apply conditional formatting based on state
            if rec.state == 'sale':
                sheet.write(row, 11, rec.state.capitalize(), workbook.add_format({'bg_color': '#90EE90'}))  # Light green for sale
            elif rec.state == 'draft':
                sheet.write(row, 11, rec.state.capitalize(), workbook.add_format({'bg_color': '#ECFF33'}))  # Light yellow for draft
            elif rec.state == 'cancel':
                sheet.write(row, 11, rec.state.capitalize(), workbook.add_format({'bg_color': '#FFA07A'}))  # Light salmon for cancel
            row += 1

        # Write totals at the bottom
        sheet.write(row, 6, 'Total', total_format)
        sheet.write(row, 7, f"{currency_symbol}{round(column_totals[0],2)}", total_format)
        sheet.write(row, 8, f"{currency_symbol}{round(column_totals[1],2)}", total_format)
        sheet.write(row, 9, f"{currency_symbol}{round(column_totals[2],2)}", total_format)
        sheet.write(row, 14, f"{currency_symbol}{round(column_totals[3],2)}", total_format)

        #SHEET2
        sheet1 = workbook.add_worksheet('Customer Report')
        
        sheet1.set_column('A:A',5)
        sheet1.set_column('B:B',20)
        sheet1.set_column('C:G',15)
        sheet1.set_default_row(20)  
        sheet1.set_row(0, 30)
        
        report_header1 = f"Customer report from {start_date} to {end_date}"
        sheet1.merge_range('A1:G1', report_header1, header_format)
        sheet1.set_row(0, 25)  # Set row height for the header
        sheet1.set_row(1, 30)

        # Write headers with bold format
        headers = [
            'S.No','Customer', 'Count', 'Untaxed amount', 'Taxes', 'Amount Total', 'Amount to invoice'
        ]
        for i, header in enumerate(headers):
            sheet1.write(1, i, header, bold_format)
        
        # print(">>>>>>>>>>>>>>>>>>>>>>",str(self.start_date))
        query_fet = (
            "SELECT "
            "so.partner_id, "
            "rp.name AS partner_name, "
            "COUNT(so.id) AS order_count, "
            "SUM(so.amount_untaxed) AS total_amount_untaxed, "
            "SUM(so.amount_tax) AS total_amount_tax, "
            "SUM(so.amount_total) AS total_amount_total, "
            "SUM(so.amount_to_invoice) AS total_amount_to_invoice "
            "FROM sale_order so "
            "JOIN res_partner rp ON so.partner_id = rp.id "
            "WHERE so.date_order BETWEEN %s AND %s "
            "AND so.user_id = %s "
            "GROUP BY so.partner_id, rp.name"
        )

        params = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),user_id)
        self.env.cr.execute(query_fet, params)
        result_data = self.env.cr.fetchall()
        # print(result_data)
        row=2
        for ind,i in enumerate(result_data, start=1):
            sheet1.write(row, 0, ind, number_format)
            sheet1.write(row, 1, i[1], normal_format)
            sheet1.write(row, 2, f"{i[2] or '0'}", number_format)
            sheet1.write(row, 3, f"{currency_symbol}{i[3] or 'NA'}", normal_format)
            sheet1.write(row, 4, f"{currency_symbol}{i[4] or 'NA'}", normal_format)
            sheet1.write(row, 5, f"{currency_symbol}{i[5] or 'NA'}", normal_format)
            sheet1.write(row, 6, f"{currency_symbol}{i[6] or 'NA'}", normal_format)
            row+=1

        sheet2 = workbook.add_worksheet('Product Report')
        
        sheet2.set_column('A:A',5)
        sheet2.set_column('B:B',20)
        sheet2.set_column('C:H',15)
        sheet2.set_default_row(20)  
        sheet2.set_row(0, 30)
        
        report_header2 = f"Product report from {start_date} to {end_date}"
        sheet2.merge_range('A1:H1', report_header2, header_format)
        sheet2.set_row(0, 25)  # Set row height for the header
        sheet2.set_row(1, 30)

        # Write headers with bold format
        headers = [
            'S.No','Product Name','Order Id', 'Customer name', 'Current Price', 'Quantity', 'selling price','Total price'
        ]
        for i, header in enumerate(headers):
            sheet2.write(1, i, header, bold_format)
        
        query_fet = (
            "SELECT pt.name AS product_name, so.name AS order_name, rp.name AS partner_name, "
            "pt.list_price AS current_price, "
            "SUM(sol.product_uom_qty) AS total_quantity, "
            "SUM(sol.price_unit) AS unit_price, "
            "SUM(sol.price_total) AS total_price "
            "FROM sale_order so "
            "JOIN res_partner rp ON so.partner_id = rp.id "
            "JOIN sale_order_line sol ON so.id = sol.order_id "
            "JOIN product_product pp ON sol.product_id = pp.id "
            "JOIN product_template pt ON pp.product_tmpl_id = pt.id "
            "WHERE so.date_order BETWEEN %s AND %s "
            "AND so.user_id = %s "
            "GROUP BY pt.name, so.name, rp.name, so.partner_id, pt.list_price"
        )
        params = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),user_id)
        self.env.cr.execute(query_fet, params)
        result_data = self.env.cr.fetchall()

        # print(result_data)  # Debugging line to check the data
        

        row = 2  # Start from the third row
        for ind,i in enumerate(result_data, start=1):
            sheet2.write(row, 0, ind, number_format)
            sheet2.write(row, 1, f"{i[0]['en_US'] or 'NA'}", normal_format)
            sheet2.write(row, 2, f"{i[1] or 'NA'}", normal_format)
            sheet2.write(row, 3, f"{i[2] or 'NA'}", normal_format)
            sheet2.write(row, 4, f"{currency_symbol}{i[3] or 'NA'}", normal_format)
            sheet2.write(row, 5, f"{i[4] or 'NA'}", number_format)
            sheet2.write(row, 6, f"{currency_symbol}{i[5] or 'NA'}", normal_format)
            sheet2.write(row, 7, f"{currency_symbol}{i[6] or 'NA'}", normal_format)
            row += 1

        workbook.close()
        output.seek(0)

        return output.read(),True

    def run_monthly_notification(self):
        today = fields.Date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        # Now you have the starting and ending dates of the previous month
        start_date = first_day_of_previous_month
        end_date = last_day_of_previous_month
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", start_date, end_date)
        action = self.env['res.users'].search([('share', '=', False)])
        for ras in action:
            domain = [
                ('date_order', '>=', start_date),
                ('date_order', '<=', end_date),
                ('user_id','=',ras.id),
            ]
            action = self.env['sale.order'].search(domain)
            report_data,status = self.action_xlsx_report_download(action, start_date, end_date,ras.id)
            # print(self.env.user.id)
            if status:
                # Create the attachment
                attachment = self.env['ir.attachment'].create({
                    'name': f'monthly_report_for_{ras.name}_from_{start_date}_to_{end_date}.xlsx',
                    'type': 'binary',
                    'datas': base64.b64encode(report_data),
                    'res_model': 'sale.order',
                    'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                })

                # print(action)
                # Prepare email values for all records
                email_values = {
                    'email_from':f'{self.env.user.email}',
                    'email_to': f'{ras.login}',
                    'subject': f"Report for {ras.name} from {start_date} to {end_date}",
                    'attachment_ids': [(6, 0, [attachment.id])]
                }

                # Send a single email with the report attachment to all recipients
                mail_template = self.env.ref('school.mail_monthly_report_template_blog')
                mail_template.send_mail(ras.id, email_values=email_values, force_send=True)
            else:
                raise AccessError(_("OOPS! Unable to get record."))

    def print_report(self):
        print(self)
        today = fields.Date.today()
        print(today)
        start_date = today
        end_date = today
        if len(self.ids) < 1:
            data = self.env["sale.order"].search([
                ('user_id','=',self.env.user.id),
            ])
            print(data)
            report_data,status = self.action_xlsx_report_download(data, start_date, end_date,self.env.user.id)
            if status:
                # Create the attachment
                attachment = self.env['ir.attachment'].create({
                    'name': f'report_BV.xlsx',
                    'type': 'binary',
                    'datas': base64.b64encode(report_data),
                    'res_model': 'sale.order',
                    'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                })
                return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }

        else:
            report_data,status = self.action_xlsx_report_download(self, start_date, end_date,self.env.user.id)
            if status:
                # Create the attachment
                attachment = self.env['ir.attachment'].create({
                    'name': f'report_BV.xlsx',
                    'type': 'binary',
                    'datas': base64.b64encode(report_data),
                    'res_model': 'sale.order',
                    'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                })
                return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
                }
    
    def approve_to_order(self):
        print(self)
        self.env['sale.order'].browse(self.id).state = "sale"



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nick_name = fields.Char(
        string="Nick Name", readonly=True, related='sale_id.nick_name')
    
    # product_image = fields.Image(string="Product Image", related='product_id.image_1920')

    def add_download_report_action_delivery(self):
        return {
            'name': 'Download Delivery Report',
            'type': 'ir.actions.act_window',
            'res_model': 'delivery.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }


class SaleOrderLines(models.Model):
    _inherit = "sale.order.line"

    # order_line_wiz = fields.Many2many(
    #     'sale.report.wizard', string="Orders")
    extra_tags = fields.Char(string="Extra field",
                             help="enter the date when order was placed")
    is_available = fields.Boolean(
        string="Is Available", compute="_compute_available_or_not")
    product_image = fields.Image(string='Product Image' ,related='product_id.image_256')

    # product_image_256 = fields.Image(string='Product Image' ,related='product_id.image_1920')

    # def _prepare_procurement_values(self, group_id=False):
    #     values = super(
    #         SaleOrderLines, self)._prepare_procurement_values(group_id)
    #     values.update({
    #         'extra_tags': self.extra_tags
    #     })
    #     return values

    # @api.depends('product_uom_qty', 'order_id.partner_id')
    # def _compute_available_or_not(self):
    #     for rec in self:
    #         product = rec.product_id
    #         print('>>>>>>>>>>>>>>>>>>>>>>p',product)
    #         if product:
    #             product_tmpl_id = product.product_tmpl_id
    #             print('>>>>>>>>>>>>>>>>>>>ptid',product_tmpl_id)
    #             virtual_available = self.env['product.template'].browse(product_tmpl_id.id).virtual_available
    #             rec.is_available = rec.product_uom_qty <= virtual_available
    #         else:
    #             rec.is_available = False


class writeAnotherDetail(models.Model):
    _inherit = "stock.move"

    extra_tags = fields.Char(string="Extra field",
                             help="enter the date when order was placed")
    product_image = fields.Image(string="Product Image", related='product_id.image_256')


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['extra_tags']
        return fields

class AccountMove(models.Model):
    _inherit = 'account.move.line'

    product_image = fields.Image(string="Product Image", related='product_id.image_256')

class ResPartner(models.Model):
    _inherit = 'res.partner'
    commission_amount_on = fields.Float(string='Commission Amount On')
    percentage = fields.Float(string="Percentage")
    b_date = fields.Date(
        string='Birthday date'
    )
    sundry_user = fields.Boolean(string="Sunbry User")
    

    def action_send_email(self):
        self.ensure_one()
        # self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self.env.ref('school.mail_res_partner_template_blog')
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'res.partner',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def run_bday_notification(self):
        today = fields.Date.today()
        today_month_day = today.strftime('%m-%d')  # Get the month and day in 'MM-DD' format

        records = self.search([])  # Get all records
        for rec in records:
            if rec.b_date and rec.b_date.strftime('%m-%d') == today_month_day:  # Compare month and day
                email_values = {
                    'email_to': rec.email,
                    'subject': f"Happy Birthday {rec.name}"
                }
                # print(f"Happy Birthday {rec.display_name}")
                mail_template = self.env.ref('school.mail_res_partner_template_blog')
                mail_template.send_mail(rec.id, email_values=email_values, force_send=True)
                # print(f"Happy Birthday {rec.display_name} Again")

class SaleOrderLines(models.Model):
    _inherit = "hr.expense"

    def print_report(self):
        # print("<<<<<<<<<<<<>>>>>>>>>>>>",self.ids)
        if len(self.ids) < 1:
            data = self.env["hr.expense"].search([])
            print(data)
            action = self.env.ref('school.action_hr_expence').with_context(my_report = True, order_lines = data).report_action(data)
            return action
        else:
            action = self.env.ref('school.action_hr_expence').with_context(my_report = True, order_lines = self).report_action(self)
            return action

class PosOrder(models.Model):
    _inherit = "pos.order"

    custom_note = fields.Text(
        string="Order Note")
    discount = fields.Boolean(string="Discount")

    location = fields.Char(string="Location", readonly=True)
    

    @api.model
    def _order_fields(self,ui_order):
        order_result = super(PosOrder, self)._order_fields(ui_order)
        order_result['custom_note'] = ui_order.get('note' or "")
        order_result['note'] = ui_order.get('note' or "")
        order_result['discount'] = ui_order.get('discount')
        order_result['location'] = ui_order.get('locatin_add')
        return order_result
    
    def get_discount(self):
        param_obj = self.env['ir.config_parameter'].sudo()
        discount_limit = param_obj.get_param('sale_discount_limit.discount_limit', default=0.0)
        return float(discount_limit)
    
    def get_location(self):
        param_obj = self.env['pos.config'].search([])
        results = []
        for i in param_obj:
            for r in i.location_ids:
                results.append(r.location)
        # print(results)
        return results
        # locations_id = param_obj.get_param('location_id', default=0.0)
        # print("<<<<<<<<<<<<<<<<<",locations_id)
        # return float(locations_id)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    is_discount_limit = fields.Boolean(string='',
        config_parameter='sale_discount_limit.is_discount_limit',
        help='Check this field for enabling discount limit', default="1")
    discount_limit = fields.Float(string='%',
        config_parameter='sale_discount_limit.discount_limit',
        help='The discount limit amount in percentage ', default=10)
    
    school_id = fields.Many2one("school.profile", string="Schools")

    location_id = fields.Many2many(
        string='Locations',
        related='pos_config_id.location_ids',
        readonly=False,
    )

    amount_limit = fields.Float(
        string="Amount Limit",
        help='Check this field for enabling discount limit', 
        config_parameter='sale_discount_limit.amount_limit',)
    

    @api.constrains('discount_limit')
    def limit(self):
        for i in self:
            if i.discount_limit:
                if i.discount_limit <= 0 or i.discount_limit > 100:
                    raise ValidationError('Field contail value between 0 & 100')
                    
class PosConfig(models.Model):
    _inherit = 'pos.config'
    location_ids = fields.Many2many('res.location', string='Locations')


# import hmac
# import hashlib
# from odoo import api, SUPERUSER_ID

# # Connect to your Odoo environment
# env = api.Environment(cr, SUPERUSER_ID, {})

# # Set your parameters
# model_name = 'mail.mail'
# email_to = 'example@example.com'
# secret_key = env['ir.config_parameter'].get_param('website_form_signature')

# # Generate the HMAC signature
# signature = hmac.new(
#     secret_key.encode('utf-8'),
#     email_to.encode('utf-8'),
#     hashlib.sha256
# ).hexdigest()

# print(signature)
