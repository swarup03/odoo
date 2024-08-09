from odoo import fields, models,api,_
from odoo.exceptions import UserError


class ProvidedCourse(models.Model):
    _name = "provided.course"
    _description = "This is course teacher model."

    number = fields.Char(string='course Reference ID', readonly=True, copy=False,
       default=lambda self: self.env['ir.sequence'].next_by_code(
           'provided.course.reference'))
    name =  fields.Char(string="Course Name")
    # booked_seats = fields.Integer(string="Booked Seats")
    # available_seats = fields.Integer(string="Available Seats", compute="_compute_available_seats")
    total_seats = fields.Integer(string="Toal Seats")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the school model"""
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code(
                    'provided.course')
        return super().create(vals_list)