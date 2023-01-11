from flectra import models, fields, api, _
from flectra.exceptions import ValidationError

class UmGrades(models.Model):
    _name = "um.grades"
    marks = fields.Integer("Marks")
    name = fields.Selection([('A','A'),('A-','A-'),('B+','B+'),('B','B'),('B-','B-'),('C+','C+'),('C','C'),('C-','C-'),('D+','D+'),('D','D'),('F','F'),('I','I')],default="A")
    weightage = fields.Float('Weightage')
    
    @api.onchange('name')
    def select_weightage(self):
        if self.name == "A":
            self.weightage = 4.00
        elif self.name == "A-":
            self.weightage = 3.67
        elif self.name == "B+":
            self.weightage = 3.33
        elif self.name =="B":
            self.weightage = 3.00
        elif self.name == "B-":
            self.weightage = 2.67
        elif self.name == "C+":
            self.weightage = 2.33
        elif self.name == "C":
            self.weightage = 2.00
        elif self.name == "C-":
            self.weightage= 1.67
        elif self.name == "D+":
            self.weightage = 1.33
        elif self.name == "D":  
            self.weightage = 1.00
        else:
            self.weightage = 0.00
            
            
            
            
            