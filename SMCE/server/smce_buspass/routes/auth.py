from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from smce_buspass import db, models
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
import smce_buspass
bcrypt = Bcrypt()
auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_no = request.form.get('id_no')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        role = request.form.get('role')
        
        if role == "incharge":
            user = models.Bus_incharge.query.filter_by(id_no=id_no).first()
            if not user or not bcrypt.check_password_hash(user.password, password):
                flash("Please check your login details.")
                return redirect(url_for("auth.login"))
            login_user(user, remember=remember)
            return redirect(url_for("home.main"))
        
        if role == "student" or role == "teacher":
            user = models.User.query.filter_by(id_no=id_no).first()
            if not user or not bcrypt.check_password_hash(user.password, password):
                flash("Please check your login details.")
                return redirect(url_for("auth.login"))
            login_user(user, remember=remember)
            return redirect(url_for("home.main"))
        if role == "HOD":
            user = models.HOD.query.filter_by(id_no=id_no).first()
            if not user or not bcrypt.check_password_hash(user.password, password):
                flash("Please check your login details.")
                return redirect(url_for("auth.login"))
            login_user(user, remember=remember)
            return redirect(url_for("home.main"))
        else :
            jsonify("Please check your login details.")
    return render_template("login.html", title="Login Page")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        id_no = request.form.get('id_no')
        password = request.form.get('password')
        forget_password_question = request.form.get('forget_password_question')
        forget_password_answer = request.form.get('forget_password_answer')
        role = request.form.get('role')
        
        if role == "incharge":
            if not models.Bus_incharge.query.filter_by(id_no=id_no).first():
                new_user = models.Bus_incharge(
                    name=name,
                    id_no=id_no,
                    password=bcrypt.generate_password_hash(password).decode('utf-8'),
                    forget_password_question=forget_password_question,
                    forget_password_answer=forget_password_answer
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("auth.login"))
            else:
                flash("Entered ID number is already registered.")
                return redirect(url_for("auth.signup"))
        
        if role == "student" or "teacher":
            if not models.User.query.filter_by(id_no=id_no).first():
                new_user = models.User(
                    name=name,
                    id_no=id_no,
                    password=bcrypt.generate_password_hash(password).decode('utf-8'),
                    forget_password_question=forget_password_question,
                    forget_password_answer=forget_password_answer
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("auth.login"))
            else:
                flash("Entered ID number is already registered.")
                return redirect(url_for("auth.signup"))

    return render_template("signup.html", title="Signup Page", error="")

@auth.route('/incharge_forget_password', methods=['POST'])
def forget_password():
    id_no = request.form.get('id_no')
    forget_password_question = request.form.get('forget_password_question')
    forget_password_answer = request.form.get('forget_password_answer')
    
    if not all([id_no, forget_password_question, forget_password_answer]):
        flash("Please fill all the fields.")
        return redirect(url_for('auth.forget_password'))  # Update with appropriate route
    
    user = models.Bus_incharge.query.filter_by(
        id_no=id_no, 
        forget_password_question=forget_password_question, 
        forget_password_answer=forget_password_answer
    ).first()
    
    if user:
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([password, confirm_password]):
            flash('Please enter all the fields.')
            return redirect(url_for('auth.forget_password'))  # Update with appropriate route
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('auth.forget_password'))  # Update with appropriate route
        
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        
        flash('Password changed successfully.')
        return redirect(url_for('auth.login'))  # Update with appropriate route
    
    flash('Incorrect ID number or forget password answer.')
    return redirect(url_for('auth.forget_password'))  # Update with appropriate route

@auth.route('/staff_request', methods=['POST']) 
@login_required
def staff_request():
    if request.method == 'POST':
        name=request.form.get('name')
        department = request.form.get('department')
        roll_mumber = request.form.get('roll_number') 
        address = request.form.get('address')
        contact_no = request.form.get('contact_no')
        bording_point = request.form.get('bording_point')
        father = request.form.get('father')
        mother = request.form.get('mother')
        gender = request.form.get('gender')
        semester = request.form.get('semester')
        staff_id = request.form.get('staff_id')

        if not all([name,department,roll_mumber,address,contact_no,bording_point,father,mother,gender,semester,staff_id]):
            jsonify({"message": "Please fill all the fields"})

        else:
            new_request = models.BusPass_teacher_Request(
                name=name,
                department=department,
                roll_number=roll_mumber,
                address=address,
                contact_no=contact_no,
                bording_point=bording_point,
                father=father,
                mother=mother,
                gender=gender,
                semester=semester,
                staff_id=staff_id
            )
            db.session.add(new_request)
            db.session.commit()

            return jsonify({"message": "Request submitted successfully"}), 200
@auth.route('/show_staff_request', methods=['GET'])
def show_staff_request():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 10

        requests = models.BusPass_teacher_Request.query.order_by(models.BusPass_teacher_Request.id.desc()).paginate(page=page, per_page=per_page)

        data = [{
            "name": req.name,
            "department": req.department,
            "roll_number": req.roll_number,
            "address": req.address,
            "contact_no": req.contact_no,
            "bording_point": req.bording_point,
            "father": req.father,
            "mother": req.mother,
            "gender": req.gender,
            "semester": req.semester,
            "staff_id": req.staff_id,
            "created_at": req.created_at
        } for req in requests.items]

        return jsonify({
            "requests": data,
            "total": requests.total,
            "pages": requests.pages,
            "current_page": requests.page,
            "next_page": requests.next_num,
            "prev_page": requests.prev_num
        }), 200
      
@auth.route('/hod_request', methods=['POST']) 
@login_required
def hod_request():
    if request.method == 'POST':
        name=request.form.get('name')
        department = request.form.get('department')
        roll_mumber = request.form.get('roll_number') 
        address = request.form.get('address')
        contact_no = request.form.get('contact_no')
        bording_point = request.form.get('bording_point')
        father = request.form.get('father')
        mother = request.form.get('mother')
        gender = request.form.get('gender')
        semester = request.form.get('semester')
        register_number = request.form.get('register_number')

        if not all([name,department,roll_mumber,address,contact_no,bording_point,father,mother,gender,semester,register_number]):
            jsonify({"message": "Please fill all the fields"})

        else:
            new_request = models.BusPass_student_Request(
                name=name,
                department=department,
                roll_number=roll_mumber,
                address=address,
                contact_no=contact_no,
                bording_point=bording_point,
                father=father,
                mother=mother,
                gender=gender,
                semester=semester,
                register_number=register_number
            )
            db.session.add(new_request)
            db.session.commit()

            return jsonify({"message": "Request submitted successfully"}), 200

@auth.route('/show_hod_request', methods=['GET'])
def show_hod_request():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 10

        requests = models.BusPass_student_Request.query.order_by(models.BusPass_student_Request.id.desc()).paginate(page=page, per_page=per_page)

        data = [{
            "name": req.name,
            "department": req.department,
            "roll_number": req.roll_number,
            "address": req.address,
            "contact_no": req.contact_no,
            "bording_point": req.bording_point,
            "father": req.father,
            "mother": req.mother,
            "gender": req.gender,
            "semester": req.semester,
            "staff_id": req.staff_id,
            "created_at": req.created_at
        } for req in requests.items]

        return jsonify({
            "requests": data,
            "total": requests.total,
            "pages": requests.pages,
            "current_page": requests.page,
            "next_page": requests.next_num,
            "prev_page": requests.prev_num
        }), 200

@auth.route("/approve", methods=["PUT"])
@login_required
def approve():
    if request.method == 'PUT':
        request_id = request.form.get('id')

        if not request_id:
            return jsonify({"message": "Please provide request id"}), 400

        bus_request = models.BusPass_student_Request.query.get(request_id)

        if not bus_request:
            return jsonify({"message": "Request not found"}), 404

        bus_request.status = 'approved'
        db.session.commit()

        return jsonify({"message": "Request approved successfully"}), 200

@auth.route("/add_buspass", methods=["POST"])
@login_required
def add_buspass():
    if request.method == "POST":
        name = request.form.get('name')
        id_no = request.form.get('id_no')
        fathers_name = request.form.get('fathers_name')
        mothers_name = request.form.get('mothers_name')
        bus_no = request.form.get('bus_no')
        department = request.form.get('department')
        roll_number = request.form.get('roll_number')
        admission_year = request.form.get('admission_year')
        boarding_point = request.form.get('boarding_point')
        booking_date = request.form.get('booking_date')
        validity_date = request.form.get('validity_date')
        amount = request.form.get('amount')
        student_image = request.files.get('student_image')
        student_signature = request.files.get('student_signature')
        incharge_signature = request.files.get('incharge_signature')
        principal_signature = request.files.get('principal_signature')
        college_seal = request.files.get('college_seal')

        # Check if all fields are filled
        if not all([name,id_no,fathers_name,mothers_name,bus_no, department, roll_number, admission_year, boarding_point, booking_date, validity_date, amount, student_image, student_signature, incharge_signature, principal_signature, college_seal]):
            flash("Please fill all the fields")
            return redirect(url_for('auth.add_buspass'))

        # Save images if they are within the allowed size
        def save_file(file):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(smce_buspass.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                return filename
            else:
                flash("Invalid file type or file size exceeds limit")
                return None

        student_image_filename = save_file(student_image)
        student_signature_filename = save_file(student_signature)
        incharge_signature_filename = save_file(incharge_signature)
        principal_signature_filename = save_file(principal_signature)
        college_seal_filename = save_file(college_seal)

        # Parse dates
        booking_date_parsed = datetime.strptime(booking_date, '%Y-%m-%d')
        validity_date_parsed = datetime.strptime(validity_date, '%Y-%m-%d')

        new_buspass = models.Bus_pass(
            name=name,
            id_no=id_no,
            fathers_name=fathers_name,
            mothers_name=mothers_name,
            bus_no=bus_no,
            department=department,
            roll_number=roll_number,
            admission_year=admission_year,
            boarding_point=boarding_point,
            booking_date=booking_date_parsed,
            validity_date=validity_date_parsed,
            amount=amount,
            student_image=student_image_filename,
            student_signature=student_signature_filename,
            incharge_signature=incharge_signature_filename,
            principal_signature=principal_signature_filename,
            college_seal=college_seal_filename,
        )

        db.session.add(new_buspass)
        db.session.commit()

        flash("Bus pass added successfully!")
        return redirect(url_for('auth.view_buspass'))
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route("/delete_incharge", methods=["POST"])
@login_required
def delete_incharge():
    id_no = request.form.get('id_no')
    
    if not id_no:
        flash("Please enter the ID number")
        return redirect(url_for('auth.manage_incharge'))  # Update with appropriate route
    
    user = models.Bus_incharge.query.filter_by(id_no=id_no).first()
    
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Incharge deleted successfully.")
    else:
        flash("User not found")
    
    return redirect(url_for('auth.manage_incharge'))  # Update with appropriate route

@auth.route("/add_incharge", methods=["POST"])
@login_required
def add_incharge():
    if request.method == "POST":
        id_no = request.form.get('id_no')
        new_incharge = models.New_incharge(id_no=id_no)
        
        db.session.add(new_incharge)
        db.session.commit()
        
        flash("Incharge added successfully.")
        return redirect(url_for('auth.manage_incharge'))  # Update with appropriate route
@auth.route("/addHOD", methods=["POST"])
def addHOD():
    if request == "POST":
        name = request.form.get('name')
        id_no = request.form.get('id_no')
        Department = request.form.get('department')
        password = request.form.get('password')
        forget_password = request.form.get('forget_password')
        forget_password_answer = request.form.get('forget_password_answer')

        new_HOD = models.HOD(name=name,id_no=id_no,department=Department,password=password,forget_password=forget_password,forget_password_answer=forget_password_answer)
        db.session.add(new_HOD)
        db.session.commit()
        return jsonify({"message": "HOD added successfully"}), 200
    
@auth.route('/HOD_forget_password', methods=['POST'])
def HOD_forget_password():
    id_no = request.form.get('id_no')
    forget_password_question = request.form.get('forget_password_question')
    forget_password_answer = request.form.get('forget_password_answer')
    
    if not all([id_no, forget_password_question, forget_password_answer]):
        flash("Please fill all the fields.")
        return redirect(url_for('auth.forget_password'))  # Update with appropriate route
    
    user = models.HOD.query.filter_by(
        id_no=id_no, 
        forget_password_question=forget_password_question, 
        forget_password_answer=forget_password_answer
    ).first()
    
    if user:
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([password, confirm_password]):
            flash('Please enter all the fields.')
        
        if password != confirm_password:
            flash('Passwords do not match.')
        
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        
        flash('Password changed successfully.')
    flash('Incorrect ID number or forget password answer.')
@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
