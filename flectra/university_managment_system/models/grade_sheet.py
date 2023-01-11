from flectra import models, fields, api, _
from flectra.exceptions import ValidationError

class UmSheet(models.Model):
    _name = "um.gradesheet"
    name = fields.Date("Date")    
    semester_id = fields.Many2one(comodel_name="um.semester", string="Semester")
    course_id = fields.Many2one(comodel_name="um.course", string="Course")
    state2 = fields.Selection([('draft','Draft'), ('submitted','Submitted'),('locked','Locked'),('cancel','Cancel')], string='State',default="draft")
    student_ids = fields.One2many(comodel_name='students.grade',inverse_name='gradesheet_id',string="Students")
    
    def load_students(self):
        records = self.env["um.student"].search([])
        for rec in records:
            for sem in rec.semester_ids:
                if self.semester_id.id == sem.id:
                    if self.course_id.id in [s.name.id for s in sem.course_ids]:
                        record_exist = self.env['students.grade'].search([('name','=',rec.id),('reg_no','=',rec.reg_no),('gradesheet_id','=',self.id)])
                        if record_exist:
                            continue
                        self.env['students.grade'].create(
                            {
                                "name" : rec.id,
                                "reg_no" : rec.reg_no,
                                "gradesheet_id" : self.id,
                            }
                        )
                        
    def action_submit(self):
        if self.state2 == "draft":
            self.state2 = "submitted"
            
    def action_lock(self):
        for i in self:
          if i.state2 == "submitted":
            i.state2 = "locked"
        for stdnt in self.student_ids:
            student_id = self.env["um.student"].browse([stdnt.name.id])
            for sem in student_id.semester_ids:
                if self.semester_id.id == sem.name.id:
                    for crs in sem.course_ids:
                        if self.course_id.id == crs.name.id:
                            crs.grades = stdnt.grades
                            crs.weightage = stdnt.weightage
                        
        
            
    def action_cancel(self):
        if self.state2 =="submitted" or self.state2=="locked":
            self.state2 = "cancel"
            
    def action_reset(self):
        if self.state2 == "cancel":
            self.state2 = "draft"
    
    
class StudentGrade(models.Model):
    _name="students.grade"
    name = fields.Many2one("um.student","Name")
    reg_no = fields.Char(related="name.reg_no",string="Registration Number")
    s_marks = fields.Float("Sessional Marks")
    m_marks = fields.Float("Mids Marks")
    f_marks = fields.Float("Final Marks")
    t_marks = fields.Float("Total Marks")
    grades = fields.Char("Grade")
    weightage = fields.Float('Weightage')
    gradesheet_id = fields.Many2one("um.gradesheet")
    
    @api.onchange('grades')
    def select_weightage(self):
        if self.grades == "A":
            self.weightage = 4.00
        elif self.grades == "A-":
            self.weightage = 3.67
        elif self.grades == "B+":
            self.weightage = 3.33
        elif self.grades =="B":
            self.weightage = 3.00
        elif self.grades == "B-":
            self.weightage = 2.67
        elif self.grades == "C+":
            self.weightage = 2.33
        elif self.grades == "C":
            self.weightage = 2.00
        elif self.grades == "C-":
            self.weightage= 1.67
        elif self.grades == "D+":
            self.weightage = 1.33
        elif self.grades == "D":  
            self.weightage = 1.00
        else:
            self.weightage = 0.00
    
    @api.onchange('s_marks','m_marks','f_marks')
    def total_marks(self):
        print('\n\n\n\n Function called')
        for rec in self:
            rec.t_marks = rec.s_marks + rec.m_marks + rec.f_marks
            marks_marks = self.env["um.grades"].search([])
            marks_list = [grade.marks for grade in marks_marks]
            print("\n\n\n\n",marks_list)
            temp_marks = 0
            for i in range(0, len(marks_list)):
                if rec.t_marks >= max(marks_list):
                    temp_marks = max(marks_list)
                    print("Hello world",temp_marks)
                    break
                else:
                    marks_list.remove(max(marks_list))
            grade_name = self.env["um.grades"].search([('marks','=',temp_marks)],limit=1)
            rec.grades = grade_name.name
            rec.weightage = grade_name.weightage
            
    
        