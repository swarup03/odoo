from odoo import fields, models,api,_


class SchoolTeacher(models.Model):
    _name = "school.subject"
    _description = "This is school subject model."

    name = fields.Char(string="Subject Name", required=True, help="Enter the name of the subject")
    code = fields.Char(string="Code", help="Enter the code of the subject", readonly=True)
    teacher_ids = fields.Many2many('school.teacher', string="Teachers", required=True, help="Select the teachers for the subject")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the school model"""
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'school.subject')
        return super().create(vals_list)

