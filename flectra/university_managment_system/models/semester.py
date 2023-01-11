from flectra import models, fields, api
from flectra.exceptions import ValidationError

class UmSemester(models.Model):
    _name = 'um.semester'
    name = fields.Char('Name')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    no_of_courses = fields.Integer('No. of Courses',compute="compute_courses")
    course_ids = fields.One2many(comodel_name='semester.course',inverse_name='semester_id',string="Courses")
    sch = fields.Float(string="Semester Credit Hours" ,compute="compute_sch")
    
   
    
    def compute_sch(self):
        count = 0
        for i in self.course_ids:
            count = count + i.credit_hour
        self.sch = count
        
    
    
    
    def compute_courses(self):
        for rec in self:
           if rec.course_ids:
               rec.no_of_courses = len(rec.course_ids)
           else:
               rec.no_of_courses = 0
               
    @api.onchange('start_date','end_date')
    def compare_date(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date should be less than end date')