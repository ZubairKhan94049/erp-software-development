from flectra import models, fields, api, _
from flectra.exceptions import ValidationError

class UmStudent(models.Model):
    _name = "um.student"
   # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student"
    #_inherits = {"res.partner": "partner_id"}
    
    reg_no = fields.Char("Registration No", size=20)
    name = fields.Char("name" ,size=128, translate=True)
    father_name = fields.Char("Father's Name")
   
    birth_date = fields.Date('Birth Date')
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', required=True, default='m')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one('res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    language = fields.Char('Language', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    partner_id = fields.Many2one('res.partner', 'Partner',required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    category_id = fields.Many2one('op.category', 'Category')
    #course_detail_ids = fields.One2many('op.student.course', 'student_id','Course Details',tracking=True)
    active = fields.Boolean(default=True)
    mobile = fields.Integer("Mobile")
    phone = fields.Integer("Phone")
    email = fields.Char("Email")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state',  string="Fed. State")
    country_id = fields.Many2one('res.country',  string="Country")
    permanent_address = fields.Char(string='Permanent Address')
    program_id = fields.Many2one("um.program",string="Program")
    plan_id = fields.Many2one(related="program_id.plan_id",string="Plan")
    batch_id = fields.Many2one('um.batch','Batch')
    semester_ids = fields.One2many(comodel_name="student.semester",inverse_name="student_id",string="Semester")
    
    @api.onchange('batch_id')
    def find_semester(self):
        for semester in self.batch_id.semester_id:
             x = self.env['student.semester'].create(
                 {
                     "name" : semester.id,
                     "start_date" : semester.start_date,
                     "end_date" : semester.end_date,
                     "student_id": self.id,
                 }
        
             )
             for course in semester.course_ids:
                 self.env['student.course'].create(
                 {
                     "name" : course.name.id,
                     "semester_id": x.id,
                 }
        
             )   
        
    

    _sql_constraints = [(
        'unique_reg_no',
        'unique(reg_no)',
        'REG no Number must be unique per student!'
    )]


    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id
    
    same_as_above = fields.Boolean('Same as above?')
    partner_id = fields.Many2one('res.partner', 'Related Contact',
                                 required=True, ondelete="cascade")
    
    p_street = fields.Char()
    p_street2 = fields.Char()
    p_zip = fields.Char()
    p_city = fields.Char()
    p_state_id = fields.Many2one('res.country.state',  string="Fed. State")
    p_country_id = fields.Many2one('res.country',  string="Country")
    permanent_address = fields.Char(string='Permanent Address')

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    )]
    
    @api.onchange('same_as_above')
    def onchange_is_check (self):
        if self.same_as_above == True:
            self.p_street= self.street
            self.p_street2= self.street2
            self.p_zip= self.zip
            self.p_city= self.city
            self.p_state_id= self.state_id
            self.p_country_id= self.country_id
        else:
            self.p_street= False
            self.p_street2= False
            self.p_zip= False
            self.p_city= False
            self.p_state_id= False
            self.p_country_id= False
            
    def student_action_view(self):
        user = self.env.user
        if user.has_group('university_managment_system.group_cms_faculity') or user.has_group('university_managment_system.group_cms_admin'):
            return {
                'name': "Students",
                'res_model': 'um.student',
                'type': 'ir.actions.act_window',
                'view_mode': 'kanban,tree,graph,pivot,form', 
                'target': 'current', 
            }
        elif user.has_group('university_managment_system.group_cms_student') and not user.has_group('university_managment_system.group_cms_faculity') and not user.has_group('university_managment_system.group_cms_admin'):
            own_recod = self.env['um.student'].search([('user_id','=',user.id)],limit=1)
            domain = [('id','=',  own_recod.id)]
            return {
                'name': "Students",
                'res_model': 'um.student',
                'type': 'ir.actions.act_window',
                'view_mode': 'kanban,tree,form', 
                'context':{'create': False,'delete':False,'edit':False},
                'domain': domain,
                'target': 'current', 
            }

class StudentSemeter(models.Model):
    _name = "student.semester"
    name = fields.Many2one(string="Name",comodel_name="um.semester")
    start_date = fields.Date(realted="name.start_date",string="Start Date")
    end_date = fields.Date(realted="name.end_date",string="End Date")
    no_of_courses = fields.Integer(string="No. of courses", compute="compute_courses")
    course_ids = fields.One2many(comodel_name='student.course',inverse_name='semester_id',string="Courses")
    student_id = fields.Many2one(comodel_name='um.student')
    sch = fields.Float(string="Semester Credit Hours" ,compute="compute_sch", store=True)
    sgp = fields.Float(string="Semester Grade points" ,compute="compute_sgp", store=True)
    
   
    @api.depends('course_ids','course_ids.credit_hour')
    def compute_sch(self):
        print('\n\n\n\n\n\n\n i am here')
        for sem in self:
            count = 0
            for i in sem.course_ids:
                count = count + i.credit_hour
            sem.sch = count
            
    @api.depends('course_ids','course_ids.weightage','course_ids.credit_hour')
    def compute_sgp(self):
        print('\n\n\n\n\n\n\n i am here')
        for sem in self:
            count = 0
            for i in sem.course_ids:
                count = count + (i.credit_hour * i.weightage )
            sem.sgp = count
    
    def compute_courses(self):
        for rec in self:
           if rec.course_ids:
               rec.no_of_courses = len(rec.course_ids)
           else:
               rec.no_of_courses = 0