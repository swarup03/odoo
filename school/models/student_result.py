from odoo import fields, models, api,_
from odoo.exceptions import UserError


class StudentResult(models.Model):
    _name = "student.result"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = "Student Result Model"

    number = fields.Char(string='Reference', readonly=True,tracking=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'class.teacher.reference'))
    student_id = fields.Many2one('school.student', string="Student", readonly=True)
    subject_id = fields.Many2one('school.subject', string="Subject", readonly=True)  # Add this field
    status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string="Status", default='pending', readonly=True, tracking=True)
    percentage = fields.Float(string="Percentage", help="Percentage of marks obtained", readonly=True, tracking=True)

    # def unlink(self):
    #     raise UserError(_('You cannot delete the student result recurds.'))

    def copy(self, default=None):
        raise UserError(_('You cannot duplicate the student result recurds.'))
    
    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model"""
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code(
                    'student.result')
        return super().create(vals_list)