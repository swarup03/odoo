from odoo import fields, models, api, _


class NotifyRemoveData(models.TransientModel):
    _name = 'notify.remove.data.wizard'
    _description = "This is a notification before removing student records."

    # @api.model_create_multi
    def remove_student_actions(self):
        # Call the remove_student method of the SchoolStudent model
        # self.env['school.student'].remove_student()
        # return {'type': 'ir.actions.act_window_close'}
        print("this is wizard in odoo17")
        return True
