from odoo import fields, models,api,_
from odoo.exceptions import UserError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "This is school teacher model."
    _inherit = "school.person"

    number = fields.Char(string='Teacher Reference ID', readonly=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'class.teacher.reference'))
    join_date = fields.Date(string="Join Date", required=True, help="Enter the joining date of the teacher")
    salary = fields.Monetary(string="Salary", help="Enter the salary of the teacher")
    currency_id = fields.Many2one(comodel_name='res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]).id)
    subject = fields.Many2one("school.subject", string="Subject", required=True, help="Select the subject of the teacher", store=True)
    school_id = fields.Many2one("school.profile", string="School", required=True, help="Select the school of the teacher", store=True,
        ondelete='restrict')
    # abs = fields.Float(string="demp", compute="_compute_count_abs")
    # sba =fields.Float(string="sba")
    
    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the teacher model"""
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code(
                    'school.teacher')
        
        # action = self.env['res.users'].browse(self.env.user.id)
        # print(action)
        # user = self.env.user

        # # Determine if the user is a manager
        # is_manager = user.has_group('school.group_school_teacher_record_access')
        # print(is_manager)


        return super().create(vals_list)




    
    # @api.depends('salary')
    # def _compute_count_abs(self):
    #     for line in self:
    #         line.abs = line.salary / 2
    # @api.onchange('salary')
    # def _onchange_count_sba(self):
    #     self.sba = self.salary/2
