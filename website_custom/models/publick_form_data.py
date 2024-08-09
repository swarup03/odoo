from odoo import fields, models,api,_
from odoo.exceptions import UserError

class publicData(models.Model):
    _name = "public.data"
    _description = "This is task for puclic user."

    email = fields.Char(string='Email')
    password =  fields.Char(string="Password")
