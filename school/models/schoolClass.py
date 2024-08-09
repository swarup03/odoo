from odoo import fields, models, api


class SchoolClass(models.Model):
    _name = "school.class"
    _description = "This is class profile."

    name = fields.Char(string="Class Name", required=True, help="Enter the name of the class")
    capacity = fields.Integer(string="Capacity",default=30 , help="Enter the maximum capacity of the class")
    student_id = fields.One2many("school.student", "class_id", string="Students", readonly=True)
    teachers = fields.Many2one("school.teacher", string="Class teacher",domain="[('school_id','=',schools)]", help="Select the teacher for the class")
    schools = fields.Many2one("school.profile", string="School name", help="Select the school for the class")
    total_students = fields.Integer(string="Total Students", compute="_compute_total_students", store=True, help="Total number of students in the class")

    @api.depends('student_id')
    def _compute_total_students(self):
        for record in self:
            record.total_students = len(record.student_id)