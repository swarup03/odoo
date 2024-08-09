from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class SchoolPerson(models.AbstractModel):
    _name = "school.person"
    _description = "This is a base model for school persons."

    name = fields.Char(string="Name", required=True, help="Enter the name of the student", translate=True)
    photo = fields.Binary(string="Photo", help="Upload the photo of the student")
    signature = fields.Binary(string='Signature')
    email = fields.Char(string="Email", help="Enter the email address of the student")
    phone = fields.Integer(string="Phone", help="Enter the phone number of the student")
    
    # Adding unique constraint to email field
    _sql_constraints = [
        ('unique_email', 'unique(email,phone)', "Email must be unique."),
        
    ]
    date_of_birth = fields.Date(string="Date of Birth", help='Enter the date of birth.', required=True)
    age = fields.Integer(string="Age", help="Age of the student", compute='_compute_age', store=True, readonly=True)
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
        ("others", "Others")
    ], string="Gender", help="Select the gender of the student")

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                dob = fields.Date.from_string(record.date_of_birth)
                today = fields.Date.context_today(record)
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                record.age = age
            else:
                record.age = 0
    
    @api.constrains('age')
    def _age_constrains(self):
        if self.age < 6:
            raise ValidationError("Age should be grater than 6")

    