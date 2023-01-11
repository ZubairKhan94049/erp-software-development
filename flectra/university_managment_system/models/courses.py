from flectra import models, fields, api, _
from flectra.exceptions import ValidationError

class UmCourse(models.Model):
    
    _name = "um.course"
    #_inherit = "mail.thread"
    _description = "Course"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', size=16, required=True)
    type = fields.Selection([('theory','Theory'),('lab','Lab')],'Type')
    credit_hour = fields.Integer('Credit Hours')
    contact_hour = fields.Integer('Contact Hours')
    repeated = fields.Boolean("Repeat")
    
    semester_id = fields.Many2one(comodel_name='um.semester',string="Semester")
    grades = fields.Char(string = "Grades")
    
    
class StudentCourse(models.Model):
    
    _name = "student.course"
    _description = "Course"

    name = fields.Many2one('um.course',string='Name', required=True)
    code = fields.Char('Code', related="name.code",size=16, required=True)
    type = fields.Selection([('theory','Theory'),('lab','Lab')],'Type',related="name.type")
    credit_hour = fields.Integer('Credit Hours',related="name.credit_hour")
    contact_hour = fields.Integer('Contact Hours',related="name.contact_hour")
    repeated = fields.Boolean("Repeat")
    
    semester_id = fields.Many2one(comodel_name='student.semester',string="Semester")
    grades = fields.Char(string = "Grade")
    weightage = fields.Float('Weightage')
    
    
            
class SemesterCourse(models.Model):
    
    _name = "semester.course"
    _description = "Course"

    name = fields.Many2one('um.course',string='Name', required=True)
    code = fields.Char('Code', related="name.code",size=16, required=True)
    type = fields.Selection([('theory','Theory'),('lab','Lab')],'Type',related="name.type")
    credit_hour = fields.Integer('Credit Hours',related="name.credit_hour")
    contact_hour = fields.Integer('Contact Hours',related="name.contact_hour")
    repeated = fields.Boolean("Repeat")
    
    semester_id = fields.Many2one(comodel_name='um.semester',string="Semester")
    grades = fields.Char(string = "Grade")
    weightage = fields.Float('Weightage')
    
   
    
             
                       
                        
                    
           
    