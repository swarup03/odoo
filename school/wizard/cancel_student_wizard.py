from odoo import fields, models, api, _
from odoo.exceptions import UserError

class CancelSchoolWizard(models.TransientModel):
    _name = 'cancel.school.wizard'
    _description = "This is a notification before removing students."

    password = fields.Char(string='Password')

    def cancel_school(self):
        expected_password = "school"  
        if self.password == expected_password:
            active_ids = self.env.context.get('active_ids')
            schools = self.env['school.profile'].browse(active_ids)
            schools.unlink()  # Call action_cancel to cancel the orders
            return {'type': 'ir.actions.act_window_close'}
        else:
            raise UserError('Incorrect password! Please try again.')
        