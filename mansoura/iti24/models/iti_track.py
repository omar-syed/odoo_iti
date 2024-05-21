from odoo import models,fields

class ItiTrack(models.Model):
    _name = "iti.track"
    # _rec_name = "capacity"
    
    name = fields.Char()
    is_open = fields.Boolean()
    capacity = fields.Integer()
    student_ids = fields.One2many(comodel_name="met.student",inverse_name="track_id") #logcal