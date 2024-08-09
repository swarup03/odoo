from odoo import fields, models,api,_
from odoo.exceptions import ValidationError
import pdb

class ProvidedCourseLine(models.Model):
    _name = "provided.course.line"
    _description = "This is course line teacher model."

    school_id = fields.Many2one('school.profile',string="school")
    course_id =  fields.Many2one('provided.course',string="Course Namem")
    total_student = fields.Integer(string="No. Student")

    @api.model_create_multi
    def create(self, vals_list):
        records =super().create(vals_list)
        for record in records:
            course_obj = self.env['provided.course'].browse(record.course_id.id)
            new_number = course_obj.total_seats - record.total_student
            # print(new_number)
            if new_number >= 0:
                course_obj.write({
                    'total_seats': new_number,
                })
            else:
                raise ValueError(_(f"For {course_obj.name} only {course_obj.total_seats} available"))
        return records

    def write(self, vals):
        if 'course_id' in vals:
            raise ValueError(_("You cannot change the course"))
        
        if 'total_student' in vals:
            student_result_obj = self.env['provided.course'].browse(self.course_id.id)
            new_number = student_result_obj.total_seats - vals['total_student'] + self.total_student

            if new_number >= 0:
                student_result_obj.write({
                    'total_seats': new_number,
                })
            else:
                raise ValueError(_("Quantity not available"))
        
        return super().write(vals)


    def unlink(self):
        for record in self:
            student_result_obj = self.env['provided.course'].browse(record.course_id.id)
            new_number = record.total_student + student_result_obj.total_seats
            student_result_obj.write({'total_seats': new_number})

        result = super(ProvidedCourseLine, self).unlink()
        # print(result)
        return result