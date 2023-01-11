from flectra import models, fields, api, _
from flectra.exceptions import ValidationError

class Umplan(models.Model):
    _name = 'um.plan'
    name = fields.Char('Plan')