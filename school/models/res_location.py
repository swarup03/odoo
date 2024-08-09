from odoo import fields, models,api
from odoo.exceptions import UserError


class SchoolTeacher(models.Model):
    _name = "res.location"
    _description = "This is Location for POS."

    _rec_name ='location'
    # locations = fields.Selection([("sc", "Science City"),("sbr", "Sindhubhavan"),("sm", "Sabarmati"),("bf", "Bhadra Fort"),("kk", "Kankaria")], string="Location")
    location = fields.Char(string="Location")
