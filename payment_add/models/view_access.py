from odoo import _, api, models, fields

class viewAccess(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        print(">>>>>>>>>>><<<<<<<<<<<<<<<<<<",arch)
        print(view)
        # print(view.xpath("//fields"))
        # active_company = self.env.user
        user_has_group = self.env.user.has_group('school.group_school_student_record_access')
        if view_type == 'form' and (user_has_group):
            for node in arch.xpath("//field"):
                node.set('readonly', '1')

            for node in arch.xpath("//form"):
                node.set('create','false')
                node.set('delete','false')

        if view_type == 'tree' and (user_has_group):
            for node in arch.xpath("//tree"):
                node.set('create','false')
                node.set('delete','false')
        return arch, view

# class viewAccessPartner(models.Model):
#     _inherit = 'res.partner'

#     @api.model
#     def _get_view(self, view_id=None, view_type='form', **options):
#         arch, view = super()._get_view(view_id, view_type, **options)
#         print(">>>>>>>>>>><<<<<<<<<<<<<<<<<<",arch)
#         print(view)
#         print(arch.xpath("//fields"))
#         # active_company = self.env.user
#         user_has_group = self.env.user.has_group('school.group_school_student_record_access')
#         if view_type == 'form' and (user_has_group):
#             for node in arch.xpath("//field"):
#                 node.set('readonly', '1')
            
#             for node in arch.xpath("//form"):
#                 node.set('create','false')
#                 node.set('delete','false')
#         return arch, view