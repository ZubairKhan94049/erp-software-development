from flectra import models, fields, api


class UmDegree(models.Model):
    _name = "um.degree"
    
    reg_number = fields.Char('Registration')
    name = fields.Char('Name')
    fname = fields.Char('Father Name')
    batch = fields.Integer("Batch")
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    checklist = fields.Many2many("degree.checklist")
    
    verfied = fields.Boolean()
    
    @api.onchange('checklist')
    def sizeofchecklist(self):

        if (len(self.checklist) == len(self.env['degree.checklist'].search([]))):
            self.verfied = True
        else:
            self.verfied = False
        
        
        print('\n\n')
        print("Verified = ", self.verfied)
        print("How many chek  = ", len(self.checklist))
        print("How many total  = ", len(self.env['degree.checklist'].search([])))
        print('\n\n')
    

class DegreeChecklist(models.Model):
    _name = "degree.checklist"
    
    name = fields.Char("Name")
    