from odoo import fields, models

class BrainvireInfotech(models.Model):
    _name = "office"
    _description = "this is the info of office"

    name = fields.Char(string="name")
    department = fields.Char(string="dep")
    floor = fields.Integer(string="floor")
