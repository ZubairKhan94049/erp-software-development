from flectra import models, fields, api, _
from flectra.exceptions import ValidationError

class UmBatch(models.Model):
    _name="um.batch"
    name = fields.Char('Batch')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    semester_id = fields.Many2many(comodel_name='um.semester',string='Semester')
    program_id = fields.Many2many(comodel_name='um.program',string='Program')
    