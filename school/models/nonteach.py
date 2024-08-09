from odoo import fields, models,api
from odoo.exceptions import UserError


class SchoolTeacher(models.Model):
    _name = "school.nonteacher"
    _description = "This is school Non teaching model."
    _inherit = "school.person"

    join_date = fields.Date(string="Join Date", required=True, help="Enter the joining date of the employee")
    salary = fields.Monetary(string="Salary", help="Enter the salary of the employee")
    currency_id = fields.Many2one(comodel_name='res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'INR')]).id,readonly=True)
    school_id = fields.Many2one("school.profile", string="School", required=True, help="Select the school of the employee")