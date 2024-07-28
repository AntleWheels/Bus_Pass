from flask import Blueprint, render_template, redirect, url_for, request,jsonify
from flask.helpers import flash
from flask_bcrypt import Bcrypt,bcrypt
from smce_buspass import models, db
from flask_login import login_user, logout_user,login_required,current_user
from smce_buspass.models import Bus_pass,User
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
brypt = Bcrypt()
stud = Blueprint("stud", __name__, url_prefix="/stud")
@stud.route("/view_buspass", methods=["GET"])
@login_required
def view_buspass():
    buspass = Bus_pass.query.filter_by(id_no=current_user.id_no).first()
    if not buspass:
        return jsonify({"error": "No bus pass found for the logged-in user."}), 404

    buspass_details = {
        'id': buspass.id,
        'bus_no': buspass.bus_no,
        'department': buspass.department,
        'id_no': buspass.id_no,
        'admission_year': buspass.admission_year,
        'boarding_point': buspass.boarding_point,
        'booking_date': buspass.booking_date,
        'validity_date': buspass.validity_date,
        'amount': buspass.amount,
        'student_image': url_for('static', filename='uploads/' + buspass.student_image, _external=True),
        'student_signature': url_for('static', filename='uploads/' + buspass.student_signature, _external=True),
        'incharge_signature': url_for('static', filename='uploads/' + buspass.incharge_signature, _external=True),
        'principal_signature': url_for('static', filename='uploads/' + buspass.principal_signature, _external=True),
        'college_seal': url_for('static', filename='uploads/' + buspass.college_seal, _external=True),
    }

    return jsonify(buspass_details)

@stud.route('/student_forget_password', methods=['POST'])
@login_required
def forget_password():
    id_no = request.form.get('id_no')
    forget_password_question = request.form.get('forget_password_question')
    forget_password_answer = request.form.get('forget_password_answer')
    
    if not all([id_no, forget_password_question, forget_password_answer]):
        flash("Please fill all the fields.")
        return redirect(url_for('forget_password'))  # Update with appropriate route
    
    user = User.query.filter_by(
        id_no=id_no, 
        forget_password_question=forget_password_question, 
        forget_password_answer=forget_password_answer
    ).first()
    
    if user:
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([password, confirm_password]):
            flash('Please enter all the fields.')
            return redirect(url_for('forget_password'))  # Update with appropriate route
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('forget_password'))  # Update with appropriate route
        
        user.password = generate_password_hash(password)
        db.session.commit()
        
        flash('Password changed successfully.')
        return redirect(url_for('login'))  # Update with appropriate route
    
    flash('Incorrect ID number or forget password answer.')
    return redirect(url_for('forget_password'))  # Update with appropriate route

@stud.route('/User_forget_password', methods=['POST'], endpoint='auth_forget_password')
def forget_password():
    id_no = request.form.get('id_no')
    forget_password_question = request.form.get('forget_password_question')
    forget_password_answer = request.form.get('forget_password_answer')

    if not all([id_no, forget_password_question, forget_password_answer]):
        flash("Please fill all the fields.")
        return redirect(url_for('auth.forget_password'))

    user = get_user_by_credentials(id_no, forget_password_question, forget_password_answer)
    
    if user:
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([password, confirm_password]):
            flash('Please enter all the fields.')
            return redirect(url_for('auth.forget_password'))

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('auth.forget_password'))

        update_password(user, password)

        flash('Password changed successfully.')
        return redirect(url_for('auth.login'))

    flash('Incorrect ID number or forget password answer.')
    return redirect(url_for('auth.forget_password'))


def get_user_by_credentials(id_no, question, answer):
    try:
        return models.User.query.filter_by(
            id_no=id_no, 
            forget_password_question=question, 
            forget_password_answer=answer
        ).first()
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"Error querying user: {e}")
        return None


def update_password(user, new_password):
    try:
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"Error updating password: {e}")
        flash('An error occurred while updating the password. Please try again.')
        return redirect(url_for('auth.forget_password'))
