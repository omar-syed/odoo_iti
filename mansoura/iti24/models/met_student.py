from odoo import models,fields;


class ItiStudent(models.Model):
    _name = "met.student"
    # _log_access = False
    
    name = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    address = fields.Text()
    gender = fields.Selection(
        [('m',"male"),('f',"female")]
    )
    accepted = fields.Boolean()
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one(comodel_name='iti.track') #physical
    track_name = fields.Char(related='track_id.name')
    skills_ids = fields.Many2many('iti.skill')
    