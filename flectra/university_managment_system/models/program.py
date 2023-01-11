from flectra import models, fields, api, _
from flectra.exceptions import ValidationError

class UmProgram(models.Model):
    _name = "um.program"
    name = fields.Char('Program')
    plan_id = fields.Many2one("um.plan",string="Plan")
    
    