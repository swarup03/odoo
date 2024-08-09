from odoo import fields, models,api,_
from odoo.exceptions import UserError

class signedUser(models.Model):
    _name = "signed.data"
    _description = "This is task for puclic user."

    user_id = fields.Many2one('res.users', string="User")
    email = fields.Char(string='Email')
    password =  fields.Char(string="Password")
