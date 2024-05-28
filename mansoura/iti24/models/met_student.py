from odoo import models,fields,api;
from odoo.exceptions import UserError

class ItiStudent(models.Model):
    _name = "met.student"
    # _log_access = False
    @api.depends("salary")
    def calc_tax(self):
        for student in self:
            student.tax = student.salary * 0.20
        
    
    name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute = "calc_tax", store=True)
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
    state = fields.Selection(
        [
            ('applied','Applied'),
            ('first','First Interview'),
            ('second','Second Interview'),
            ('passed','Passed'),
            ('rejected','Rejected'),
        ],default = 'applied'
    )
    
    # _sql_constraints = [
    #     ("Unique Name","UNIQUE(name)","name aleardy exists"),
    #     ("Unique Email","UNIQUE(email)","email aleardy exists"),
    # ]
    
    @api.constrains("track_id")
    def check_track_id (self):
        track_count  = len(self.track_id.student_ids)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("track is full")
    
    @api.constrains("salary")
    def check_salary(self):
        if self.salary > 10000 :
            raise UserError("Salary is higher than 10000")
    
    # @api.model
    # def create(self,vals):
    #     new_student = super().create(vals)
    #     name_split = new_student.name.split()
    #     new_student.email = f"{name_split[0][0]}{name_split[1]}@gmail.com"
    #     return new_student
    @api.model
    def create(self,vals):
        name_split = vals['name'].split()
        vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        search_students = self.search([('email','=',vals['email'])],limit=5,offset=5)
        track = self.env['iti.track'].browse(vals['track_id'])
        if track.is_open is False:
            raise UserError("Selected track is close")
        if search_students:
            raise UserError('Email aleardy exist')
        return super().create(vals)
    
    def write(self,vals):
        if 'name' in vals:
            name_split = vals['name'].split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        super().write(vals)
    
    def unlink(self):
        for record in self :
            if record.state in ['passed','rejected']:
                raise UserError("you can't delete passed/rejected student")
        super().unlink()
            
    
    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed','rejected']:
            self.state = 'applied'
            
    def set_passed(self):
        self.state='passed'
        
    def set_rejected(self):
        self.state='rejected'
        

    @api.onchange("gender")
    def _on_change_gender(self):
        domain = {'track_id':[]}
        if not self.gender:
            self.gender = 'm'
            return{}
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