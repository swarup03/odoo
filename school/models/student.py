from odoo import fields, models,api,_
from odoo.exceptions import ValidationError
import io
import xlsxwriter
import pdb


import base64

class SchoolStudent(models.Model):
    _inherit = ["school.person","mail.thread","mail.activity.mixin"]
    _name = "school.student"
    _description = "This is school Student model."
    

    number = fields.Char(string='Student Reference ID', readonly=True,tracking=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'class.teacher.reference'))
    class_id = fields.Many2one('school.class', string="Class Room", help="Select the class of the student")
    subject_ids = fields.Many2many('school.subject', string="Subjects", help="Select the subjects of the student", tracking=True)
    enrollment_date = fields.Date(string="Enrollment Date", help="Enter the enrollment date of the student")
    school_id = fields.Many2one("school.profile", string="School", required=True, help="Select the school of the student")
    customer_details = fields.Html(string=' ', compute='_compute_customer_detail')
    total_fee = fields.Monetary(string="Total Fee", help='Total Fee payed by the student', required=True,default=0)
    currency_id = fields.Many2one(comodel_name='res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]).id)
    marks_ids = fields.One2many("student.mark", 'student_id', string="Student Marks")
    result_ids = fields.One2many("student.result","student_id",string="Results")
    student_data = fields.Selection([("removed", "Removed"),("available", "Available")], string="Result Available status", help="If field is showing removed than student result are removed or present", default="available")
    result_count = fields.Integer(string="Result count", compute="_compute_result_count")
    marks_count = fields.Integer(string="marks count", compute="_compute_marks_count")
    
    @api.depends('school_id')
    def _compute_customer_detail(self):
        for record in self:
            if record.school_id:
                record.customer_details = f"<p>{record.school_id.street}, {record.school_id.street2}<br/>{record.school_id.city}, {record.school_id.state_id.name}<br> {record.school_id.country_id.name}</p>"
            else:
                record.customer_details = "<p>No customer selected</p>"

    @api.depends('result_count')
    def _compute_result_count(self):
        for student in self:
            student.result_count = len(student.result_ids)

    @api.depends('marks_count')
    def _compute_marks_count(self):
        for student in self:
            student.marks_count = len(student.marks_ids)
            
    def action_get_marks_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stuent Marks',
            'view_mode': 'tree,form',
            'res_model': 'student.mark',
            'target':'new',
            'domain': [('student_id', '=', self.id)],
            'context': {'create': False}
        }

    def action_get_result_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stuent result',
            'view_mode': 'tree,form',
            'res_model': 'student.result',
            'target':'new',
            'domain': [('student_id', '=', self.id)],
            'context': {'create': False}
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code('school.student')

        student = super(SchoolStudent, self).create(vals)

        student_result_obj = self.env['student.result']
        student_marks_obj = self.env['student.mark']

        # Create student result record
        student_result_obj.create({
            'student_id': student.id,
            'status': 'pending'
        })

        # Create student marks records for each newly created student
        for subject in student.subject_ids:
            student_marks_obj.create({
                'student_id': student.id,
                'subject_id': subject.id
            })

        return student


    
    def remove_student(self):
        # Delete associated student result records using email and phone
        emails = self.mapped('email')
        print(emails)
        phones = self.mapped('phone')
        student_results = self.env['student.result'].search([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # student_results.ensure_one()
        print("search outcomes",student_results)
        student_marks = self.env['student.mark'].search([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # search_count_print = self.env['student.mark'].search_count([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # print(search_count_print)
        # search_read_print = self.env['student.mark'].search_read([('student_id.email', 'in', emails), ('student_id.phone', 'in', phones)])
        # print(search_read_print)
        # print("search outcomes for marks",type(student_marks),student_marks)
        # print(student_marks.subject_id)
        # print(student_marks.marks_obtained)
        unlink_outcome=student_results.unlink()
        # print("unlink outcome",unlink_outcome)
        student_marks.unlink()
        return super(SchoolStudent, self).write({'student_data':'removed'})
    
    def unlink(self):
        self.remove_student()
        super().unlink()
        return True

    def example_context(self):
        print("student",self)
        print(self.env.context.get('default_age'))
        print(self.env.context.get('default_name'))
        print(self.env.context.get('self'))
        return True
    
    def add_taxes_action(self):
        
        # return self.env['ir.actions.act_window']._for_xml_id("school_student.action_student_wizard")
        
        # return {
        #     'name': 'Add Total Fees',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'notify.remove.data.wizard',
        #     'view_mode': 'form',
        #     'target': 'new',
        # }
        user = self.env.user

        # Determine if the user is a manager
        is_teacher = user.has_group('school.group_school_teacher_record_access')
        is_gov = user.has_group('school.group_gov_record_access')
        is_owner = user.has_group('school.group_school_owner_record_access')
        is_student = user.has_group('school.group_school_student_record_access')
        # print(is_teacher)
        data = {}
        if is_teacher:
            data = {
                'default_annual_fees': 20000,
                'default_tuition_fees':300,
                'default_admission_fees':400,
                'default_transportation_fee':200,
                'default_examination_fees':200,
                'default_development_fees':300,
                'default_miscellaneous_fees':200,
            }
        elif is_gov:
            data = {
                'default_annual_fees': 300,
                'default_tuition_fees':0,
                'default_admission_fees':0,
                'default_transportation_fee':0,
                'default_examination_fees':50,
                'default_development_fees':0,
                'default_miscellaneous_fees':0,
            }
        elif is_owner:
            data = {
                'default_annual_fees': 10000,
                'default_tuition_fees':432,
                'default_admission_fees':100,
                'default_transportation_fee':100,
                'default_examination_fees':100,
                'default_development_fees':100,
                'default_miscellaneous_fees':100,
            }
        elif is_student:
            raise ValidationError("")
        return {
            'name': 'Add Total Fees',
            'type': 'ir.actions.act_window',
            'res_model': 'total.amount.tax.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context' : data
        }
    def action_send_email(self):
        self.ensure_one()
        mail_template = self.env.ref('school.mail_student_template_blog')
        
        ctx = {
            'default_model': 'school.student',
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
    def print_xlsx_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Transactions')

        bold_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter', 'bg_color': '#f2eee4',
             'border': True})
        normal_format = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'top'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'center'})
        sheet.set_column('A:B', 10)  # Adjust the width as needed
        sheet.set_column('C:C', 20)  # Adjust the width as needed
        sheet.set_column('A:G', 15)  # Adjust the width as needed
        # Set row height
        sheet.set_default_row(30)  # Adjust the height as needed
        row = 1
        col = 0

        # Write headers with bold format
        sheet.write('A1', 'ID', bold_format)
        sheet.write('B1', 'Name',bold_format)
        sheet.write('C1', 'Email', bold_format)
        sheet.write('D1', 'Phone No.', bold_format)
        sheet.write('E1', 'DOB', bold_format)
        sheet.write('F1', 'Age', bold_format)
        sheet.write('G1', 'Gender', bold_format)
        sheet.write('H1', 'Class No.', bold_format)
        sheet.write('I1', 'Subjects', bold_format)
        sheet.write('J1', 'Enrollment date', bold_format)
        sheet.write('K1', 'Student Fee', bold_format)
        sheet.write('L1', 'School', bold_format)

        for rec in self:
            sheet.write(row, col, rec.number, normal_format)
            sheet.write(row, col + 1, rec.name, normal_format)
            sheet.write(row, col + 2, rec.email, normal_format)
            sheet.write(row, col + 3, rec.phone, date_format)
            sheet.write(row, col + 4, rec.date_of_birth, normal_format)
            sheet.write(row, col + 5, rec.age, date_format)
            sheet.write(row, col + 6, rec.gender, normal_format)
            sheet.write(row, col + 7, rec.class_id.name, normal_format)
            sheet.write(row, col + 8, rec.marks_count, normal_format)
            sheet.write(row, col + 9, rec.enrollment_date, normal_format)
            sheet.write(row, col + 10, rec.total_fee, normal_format)
            sheet.write(row, col + 11, rec.school_id.name, normal_format)
            row+=1

        workbook.close()
        output.seek(0)

        # Encode the file to base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'student_report.xlsx',
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'school.student',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
    def print_report(self):
        print(self.result_ids.status)
        if self.result_ids.status == "completed":
            action = self.env.ref('school.action_report_student_template').with_context(my_report=True, order_lines=self).report_action(self)
            return action, {'status': 'pass'}
        elif self.result_ids.status == "failed":
            action = self.env.ref('school.action_report_student_template').with_context(my_report=True, order_lines=self).report_action(self)
            return action, {'status': 'fail'}
        elif self.result_ids.status == "pending":
            action = self.env.ref('school.action_report_student_template').with_context(my_report=True, order_lines=self).report_action(self)
            return action, {'status': 'pending'}
