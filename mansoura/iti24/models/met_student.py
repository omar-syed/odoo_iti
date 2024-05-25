from odoo import models,fields,api;


class ItiStudent(models.Model):
    _name = "met.student"
    # _log_access = False
    
    name = fields.Char(required=True)
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
    track_capacity = fields.Integer(related='track_id.capacity')
    skills_ids = fields.Many2many('iti.skill')
    grade_ids = fields.One2many('student.skill.line','student_id')

    @api.onchange("gender")
    def _on_change_gender(self):
        domain = {'track_id':[]}
        if self.gender == 'm':
            domain = {'track_id':[('is_open','=',True)]}
            self.salary = 10000
        else:
            self.salary = 5000
        return {'warning': {
            'title': 'Hello',
            'message': 'You Have Changed The Gender'
        },
            'domain':domain
        }


    
class ItiCourse(models.Model):
    _name = "iti.course"
    
    name = fields.Char()
    
class StudentCourseGrades(models.Model):
    _name = "student.skill.line"
    
    student_id = fields.Many2one("met.student")
    course_id = fields.Many2one("iti.course")
    grade = fields.Selection([
        ("g","good"),
        ("vg","very good"),
    ])