from flask_login import UserMixin
from . import db, bcrypt

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_no =db.Column(db.Integer,unique=True, nullable=False)
    year_and_sem =db.Column(db.Integer, nullable=False)
    bus_no =db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    forget_password_question = db.Column(db.String(100), nullable=False)   
    forget_password_answer = db.Column(db.String(100), nullable=False) 

    def __init__(self, name, id_no, year_and_sem, bus_no, password, forget_password_question, forget_password_answer):
        self.name = name
        self.id_no = id_no
        self.year_and_sem = year_and_sem
        self.bus_no = bus_no
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.forget_password_question = forget_password_question
        self.forget_password_answer = forget_password_answer
    @classmethod
    def authenticate(cls, id_no, password):
        found_user = cls.query.filter_by(id_no=id_no).first()
        if found_user:
            authenticate_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticate_user:
                return found_user
        return False
    
    @classmethod
    def userexists(cls, student_id):
        return True if cls.query.filter_by(student_id=student_id).first() else False
class New_incharge(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    id_no =db.Column(db.Integer, nullable=False)
    def __init__(self,id_no):
        self.id_no = id_no
        
class Bus_incharge(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_no =db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    forget_password_question = db.Column(db.String(100), nullable=False)   
    forget_password_answer = db.Column(db.String(100), nullable=False) 
    def __init__(self, name, bus_no,id_no, password, forget_password_question, forget_password_answer):
        self.name = name
        self.bus_no = bus_no
        self.id_no = id_no
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.forget_password_question = forget_password_question  
        self.forget_password_answer = forget_password_answer 

    @classmethod
    def authenticate(cls, id_no, password):
        found_user = cls.query.filter_by(id_no=id_no).first()
        if found_user:
            authenticate_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticate_user:
                return found_user
        return False
class BusPass_request(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(1000), nullable=False)
    Contact_no = db.Column(db.Integer, nullable=False)
    Bording_point = db.Column(db.String(100), nullable=False)
    Gender = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    def __init__(self,name,role,roll_number,Address,Contact_no,Bording_point,Gender,semester,id_no):
            self.name = name
            self.role = role
            self.roll_number = roll_number
            self.Address = Address
            self.Contact_no = Contact_no
            self.Bording_point = Bording_point
            self.Gender = Gender
            self.semester = semester
            self.id_no = id_no


class Bus_pass(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_no =db.Column(db.Integer, nullable=False)
    fathers_name =db.Column(db.String(100), nullable=False)
    mothers_name =db.Column(db.String(100), nullable=False)
    bus_no =db.Column(db.Integer, nullable=False)
    department =db.Column(db.String(100), nullable=False)
    roll_number =db.Column(db.Integer, nullable=False)
    admission_year=db.Column(db.Integer, nullable=False)
    bording_point=db.Column(db.String(100), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    validity_date = db.Column(db.Date, nullable=False)
    amount =db.Column(db.Integer, nullable=False)
    student_image = db.Column(db.LargeBinary, nullable=False)
    student_signature = db.Column(db.LargeBinary, nullable=False)
    incharge_signature =db.Column(db.LargeBinary,nullable=False)
    principal_signature =db.Column(db.LargeBinary,nullable=False)
    college_seal =db.Column(db.LargeBinary,nullable=False)

    def __init__(self,name,id_no,fathers_name,mothers_name, bus_no, department, roll_number, admission_year, bording_point, validity, booking_date, amount, student_image, student_signature, incharge_signature, principal_signature, college_seal):
        self.name = name
        self.id_no = id_no
        self.fathers_name =fathers_name
        self.mothers_name =mothers_name
        self.bus_no = bus_no
        self.department = department
        self.roll_number = roll_number
        self.admission_year = admission_year
        self.bording_point = bording_point
        self.validity_date = validity
        self.booking_date = booking_date
        self.amount = amount
        self.student_image = student_image
        self.student_signature = student_signature
        self.incharge_signature = incharge_signature
        self.principal_signature = principal_signature
        self.college_seal = college_seal

class BusPass_student_Request(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    department =db.Column(db.String(100), nullable=False)
    roll_number =db.Column(db.Integer, nullable=False)
    address =db.Column(db.String(1000), nullable=False)
    contact_no =db.Column(db.Integer, nullable=False)
    bording_point =db.Column(db.String(100), nullable=False)
    father = db.Column(db.String(100), nullable=False)
    mother = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    register_number = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), default="Pending")

    def __init__(self,name,department,roll_number,address,contact_no,bording_point,father,mother,gender,semester,register_number,status):
        self.name = name
        self.department = department
        self.roll_number = roll_number
        self.address = address
        self.contact_no = contact_no
        self.bording_point = bording_point
        self.father = father
        self.mother = mother
        self.gender = gender
        self.semester = semester
        self.register_number = register_number
        self.status = status
class BusPass_teacher_Request(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    department =db.Column(db.String(100), nullable=False)
    roll_number =db.Column(db.Integer, nullable=False)
    address =db.Column(db.String(1000), nullable=False)
    contact_no =db.Column(db.Integer, nullable=False)
    bording_point =db.Column(db.String(100), nullable=False)
    father = db.Column(db.String(100), nullable=False)
    mother = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    Staff_id = db.Column(db.String(100), nullable=False)

    def __init__(self,name,department,roll_number,address,contact_no,bording_point,father,mother,gender,semester,staff_id):
        self.name = name
        self.department = department
        self.roll_number = roll_number
        self.address = address
        self.contact_no = contact_no
        self.bording_point = bording_point
        self.father = father
        self.mother = mother
        self.gender = gender
        self.semester = semester
        self.Staff_id = staff_id

class HOD(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_no = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    forget_password = db.Column(db.String(100), nullable=False)
    forget_password_answer = db.Column(db.String(100), nullable=False)

    def __init__(self,name,id_no,department,password,forget_password,forget_password_answer):
        self.name = name
        self.id_no = id_no
        self.department = department
        self.password = password
        self.forget_password = forget_password
        self.forget_password_answer = forget_password_answer