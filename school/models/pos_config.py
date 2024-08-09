from odoo import fields, models

class PosConfig(models.Model):
    _inherit ='pos.config'

    enable_school = fields.Boolean()