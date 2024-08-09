from odoo import fields, models,api,_
from odoo.exceptions import ValidationError,UserError


class StudentMarks(models.Model):
    _name = "student.mark"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = "Student Marks Model"

    student_id = fields.Many2one('school.student', string="Student", readonly=True)
    subject_id = fields.Many2one('school.subject', string="Subject", readonly=True)
    marks_obtained = fields.Float(string="Marks", help="Enter the marks obtained by the student", tracking=True)

    @api.constrains('marks_obtained')
    def _check_marks_range(self):
        for record in self:
            if record.marks_obtained < 0 or record.marks_obtained > 100:
                raise ValidationError("Marks should be between 0 and 100.")

    @api.model_create_multi
    def write(self, vals_list):
        # print(self)
        # print(vals_list)
        for vals in vals_list:
            res = super(StudentMarks, self).write(vals)
            # print(type())
            print(res)
            student_result_obj = self.env['student.result']

            for student_mark in self:
                # Calculate total marks for the subject
                total_marks = sum(student_mark.student_id.marks_ids.filtered(lambda m: m.student_id == student_mark.student_id).mapped('marks_obtained'))
                total_subject_marks = self.env['student.mark'].search_count([('student_id', '=', student_mark.student_id.id)])
                print(total_subject_marks)
                percentage = (total_marks / (total_subject_marks * 100)) * 100 if total_subject_marks else 0

                # Update percentage and status in student result
                student_results = student_mark.student_id.result_ids.filtered(lambda r: r.subject_id == student_mark.subject_id)
                for student_result in student_results:
                    student_result.write({'percentage': percentage})
                    if percentage >= 40:
                        student_result.status = 'completed'
                    elif 0 < percentage < 40:
                        student_result.status = 'failed'
                    else:
                        student_result.status = 'pending'

                # If no existing record found, create a new one
                if not student_results:
                    existing_result = student_result_obj.search([('student_id', '=', student_mark.student_id.id)])
                    if existing_result:
                        existing_result.write({
                            'percentage': percentage,
                            'status': 'completed' if percentage >= 40 else 'failed' if 0 < percentage < 40 else 'pending',
                        })
                    else:
                        student_result_obj.create({
                            'student_id': student_mark.student_id.id,
                            'subject_id': student_mark.subject_id.id,
                            'percentage': percentage,
                            'status': 'completed' if percentage >= 40 else 'failed' if 0 < percentage < 40 else 'pending',
                        })

        return res

    # def unlink(self):
    #     raise UserError(_('You cannot delete the student marks recurds.'))

    def copy(self, default=None):
        raise UserError(_('You cannot duplicate the student marks recurds.'))
