from odoo import fields, models,api,_
from odoo.exceptions import UserError


class SchoolProfile(models.Model):
    _name = "school.profile"

    _rec_name ='number'
    # _inherit = ['mai.thread']
    _description = "This is school profile."
    
    number = fields.Char(string='Teacher Reference ID', readonly=True, copy=False)
    name = fields.Char(string="School Name", required=True, help="Enter the name of the school")
    email = fields.Char(string="Email", help="Enter the email address of the school")
    phone = fields.Integer(string="Phone", help="Enter the phone number of the school")
    organisation = fields.Selection([("government", "Government"),("private", "Private")], string="Organisation", help="Select the type of organisation", default="private")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")

    student_ids = fields.One2many("school.student",'school_id', string="No. of student",readonly=True)
    teacher_ids = fields.One2many("school.teacher",'school_id', string="No. of teacher",readonly=True)
    class_ids = fields.One2many("school.class", "schools", string="Classes", readonly=True)
    course_ids = fields.One2many("provided.course.line","school_id",string="Courses")
    student_count = fields.Integer(string="Student Count", compute="_compute_student_count", store=True)
    teacher_count = fields.Integer(string="Teacher Count", compute="_compute_teacher_count", store=True)
    class_count = fields.Integer(string="Class Count", compute="_compute_class_count", store=True)


    @api.depends('student_ids')
    def _compute_student_count(self):
        for school in self:
            school.student_count = len(school.student_ids)

    @api.depends('teacher_ids')
    def _compute_teacher_count(self):
        for school in self:
            school.teacher_count = len(school.teacher_ids)

    @api.depends('class_ids')
    def _compute_class_count(self):
        for school in self:
            school.class_count = len(school.class_ids)

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = f"{record.name} ({record.email})" if record.email else record.name
    #         result.append((record.id, name))
    #     return result

    def action_get_student_record(self):
        # Check if the action is triggered from a form view and not in create mode
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'view_mode': 'tree,form',
            'res_model': 'school.student',
            'target':'new',
            'domain': [('school_id', '=', self.id)],
            'context': {'create': False}
        }

    def action_get_class_record(self):
        # Check if the action is triggered from a form view and not in create mode
        return {
            'type': 'ir.actions.act_window',
            'name': 'Class',
            'view_mode': 'tree,form',
            'res_model': 'school.class',
            'target':'new',
            'domain': [('schools', '=', self.id)],
            'context': {'create': False}
        }

    def action_get_teacher_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teachers',
            'view_mode': 'tree,form',
            'res_model': 'school.teacher',
            'target':'new',
            'domain': [('school_id', '=', self.id)],
            'context': {'create': False}
        }


    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the school model"""
        print(self)
        print(vals_list)
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = self.env['ir.sequence'].next_by_code(
                    'school.profile')
        stat = super().create(vals_list)
        print(stat)
        return stat

    # def unlink(self):
    #     return {
    #         'name': 'Delete School',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'cancel.school.wizard',
    #         'view_mode': 'form',
    #         'target': 'new'
    #     }

    def copy(self, default=None):
        raise UserError(_('You cannot duplicate the school recurds.'))
    
    def action_confirm(self):
        self.write({'organisation': 'government'})
    
    def browse_button(self):
        #reag_group
        res = self.env['sale.order'].read_group([],['amount_total:sum','id:count'],['invoice_status'])
        print(res)
        # for i in res:
        #     print(i['age'])
        #     print(i['age_count'])
        #     print(type(i['__domain']),i['__domain'])

        # name_search
        # res = self.env['school.student'].name_search('swarup')
        # print(res)

        #default_get
        # res = self.env['school.student'].default_get(['currency_id','total_fee','name'])
        # print(res)

        #copy
        # ras =  super().copy()
        # print(ras.name)
        # rps =  super().copy({
        #     'name':'rahul-Duplicate'
        # })
        # print(rps.name)

        #context
        # context = {'default_name': 'John Doe', 'default_age': 15,'self':self}
        # res = self.env['school.student'].with_context(context).example_context()
        # print("School model",res)
    
    def action_send_email(self):
        # template_id = self.env.ref('school.mail_template_blog')  # Replace 'your_module.email_template_id' with the actual ID of your email template
        # template_id.send_mail(self.id, force_send=True)
        self.ensure_one()
        # self.order_line._validate_analytic_distribution()
        mail_template = self.env.ref('school.mail_school_template_blog')
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
    def get_school_data(self):
        data = super().search([])
        values = []
        for line in data:
            values.append({'id':line.id,'name':line.name})
        return values

    def pass_in_pos(self):
        data = super().search([])
        values = []
        for lines in data:
            # print(type(lines.phone))
            # print(lines.phone)
            values.append({
                'id':lines.number,
                'name':lines.name,
                'email':lines.email if lines.email else "Na",
                'phone':lines.phone if lines.phone > 100000000 else "Na",
                'organisation':lines.organisation,
                'zip':lines.zip if lines.zip else "Na",
                'cirt':lines.city if lines.city else "Na",
                'state':lines.state_id.name if lines.state_id.name else "Na",
                'country':lines.country_id.name if lines.country_id.name else "Na",
                'country_code':lines.country_code if lines.country_code else "Na",
                'student_count':lines.student_count if lines.student_count != 0 else "Na",
                'teacher_count':lines.teacher_count if lines.teacher_count != 0 else "Na",
                'class_count':lines.class_count if lines.class_count != 0 else "Na",
            })
        # print(values)
        return values 
        
    # def action_send_email(self):
    #     mail_template = self.env.ref(sale.mail_template_blog)
    #     mail_template.send_mail(self.id, force_send=True)
    
class OrderConfirmationButton(models.Model):
    _inherit = 'school.profile'

    def create_government(self):
        self.action_confirm()
        return True
