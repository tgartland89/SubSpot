import os
from flask import Flask, make_response, request, redirect, url_for, session, jsonify, g
from config import db, bcrypt  
from models import User, Teacher, Substitute, Request
from flask_migrate import Migrate
from faker import Faker 
from flask_cors import CORS
from functools import wraps
from sqlalchemy.orm import sessionmaker

fake = Faker()

app = Flask(__name__)
migrate = Migrate(app, db) 
CORS(app, supports_credentials=True)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subspot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

# creating user
def create_user(name, email, location, phone, role, password, profile_picture=None):
    user = User(name=name, email=email, location=location, phone=phone, role=role)
    user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user.profile_picture = profile_picture

    return user

# route for Home
@app.route('/')
def home():
    if 'user_id' in session:
        home_page_content = "Welcome to SubSpot! Find substitutes quickly for your teaching needs."
    else:
        home_page_content = "Welcome to SubSpot! Find substitutes quickly for your teaching needs."

    login_link = "<a href='/login'>Log In</a>"
    signup_link = "<a href='/signup'>Sign Up</a>"

    home_page_content += f"<br/><br/>{login_link} | {signup_link}"
    response = make_response(home_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

# route to the about page
@app.route('/about')
def about():
    about_content = "SubSpot is a site built by the son of a fourth grade teacher who was looking for alternatives to find substitute teachers quickly and efficiently."
    return about_content

# login route
def is_logged_in():
    return 'user_id' in session

# login route
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return jsonify({"error": "Login required."}), 401
        return f(*args, **kwargs)
    return decorated_function

# login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

        if content_type == 'application/json':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        if not email or not password:
            return jsonify({"error": "Missing email or password."}), 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
         session['user_id'] = user.id
         session['user_role'] = user.role
         session['user_name'] = user.name
         session['user_email'] = user.email 
         session['teacher_user_id'] = user.id  
         return jsonify({"role": user.role})
        return jsonify({"error": "Invalid email or password. Please try again."}), 401

# rote to get user_role
@app.route('/get_user_role', methods=['GET'])
def get_user_role():
    if 'user_id' not in session:
        return jsonify({"role": None})
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user:
        return jsonify({"role": user.role}) 
    else:
        return jsonify({"role": None})

# rote to get teachers
@app.route('/get_teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    teachers_data = [{"id": teacher.id, "name": teacher.name, "email": teacher.email, "location": teacher.location, "phone": teacher.phone} for teacher in teachers]
    return jsonify({"teachers": teachers_data})

# API endpoint to fetch the teacher's user ID
@app.route('/get_teacher_user_id', methods=['GET'])
@login_required
def get_teacher_user_id():
    teacher_user_id = session['teacher_user_id']
    return jsonify({"teacher_user_id": teacher_user_id})


# rote to get substitutes 
@app.route('/get_substitutes', methods=['GET'])
def get_substitutes():
    substitutes = Substitute.query.all()
    substitutes_data = [{"user_id": substitute.user_id, "name": substitute.name, "email": substitute.email, "location": substitute.location, "phone": substitute.phone, "qualifications": substitute.qualifications, "verification_id": substitute.verification_id} for substitute in substitutes]
    return jsonify({"substitutes": substitutes_data})

# rote to get substitutes by ID
@app.route('/substitute/<int:substitute_id>', methods=['GET'])
def get_substitute_details(substitute_id):
    substitute = Substitute.query.filter_by(user_id=substitute_id).first()
    if substitute:
        return jsonify({
            "user_id": substitute.user_id,
            "name": substitute.name,
            "email": substitute.email,
            "location": substitute.location,
            "phone": substitute.phone,
            "qualifications": substitute.qualifications,
            "verification_id": substitute.verification_id
        })
    else:
        return jsonify({"error": "Substitute not found."}), 404

# route to make_request from Teacher to Sub
# route to make_request from Teacher to Sub
@app.route('/make_request', methods=['POST'])
@login_required
def make_request():
    if request.method == 'POST':
        data = request.get_json()
        substitute_user_id = data.get('substitute_id')  
        teacher_name = session['user_name']
        teacher_email = session['user_email']

    
        new_request = Request(
            teacher_user_id=session['teacher_user_id'],  
            substitute_user_id=substitute_user_id,  
            course_being_covered='Your Course',  
            confirmation=False,
            message_sub_sent_to='',
            teacher_if_declined=False,
            school_name='Your School Name',  
            teacher_school_location='Your School Location',  
        )
        db.session.add(new_request)
        db.session.commit()

        return jsonify({"message": "Request sent successfully."})


# route to confirm_request from Sub to Teaceher  
@app.route('/confirm_request/<int:request_id>', methods=['POST'])
@login_required
def confirm_request(request_id):
    request = Request.query.get(request_id)
    if request and request.substitute_id == session['user_id']:
        request.status = 'confirmed'
        db.session.commit()
        return jsonify({"message": "Request confirmed successfully."})
    else:
        return jsonify({"error": "Invalid request or unauthorized access."}), 401

# route to deny_request from Sub to Teaceher
@app.route('/deny_request/<int:request_id>', methods=['POST'])
@login_required
def deny_request(request_id):
    request = Request.query.get(request_id)
    if request and request.substitute_id == session['user_id']:
        request.status = 'denied'
        db.session.commit()
        return jsonify({"message": "Request denied successfully."})
    else:
        return jsonify({"error": "Invalid request or unauthorized access."}), 401

# route for signup
@app.route('/auth/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        role = request.json.get('role')

        if role == 'Teacher':
            return signup_teacher()  
        elif role == 'Substitute':
            return signup_substitute()  

    return "Sign Up Form"

# route fo signup for teacher 
@app.route('/auth/signup-teacher', methods=['POST'])
def signup_teacher():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')
    location = request.json.get('location')
    phone = request.json.get('phone')
    school_name = request.json.get('school_name')
    school_location = request.json.get('school_location')  
    course_name = request.json.get('course_name')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400

    new_user = create_user(name, email, location, phone, 'Teacher', password)
    db.session.add(new_user)
    db.session.commit()

    new_teacher = Teacher(user=new_user, name=name, email=email, location=location, phone=phone,
                          school_name=school_name, school_location=school_location, course_name=course_name)
    db.session.add(new_teacher)
    db.session.commit()

    return jsonify(message=signup_confirmation_message('Teacher'))

# route fo signup for substitute
@app.route('/auth/signup-substitute', methods=['POST'])
def signup_substitute():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')
    location = request.json.get('location')
    phone = request.json.get('phone')
    qualifications = request.json.get('qualifications')
    verification_id = request.json.get('verification_id')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400

    new_user = create_user(name, email, location, phone, 'Substitute', password)
    db.session.add(new_user)
    db.session.commit()

    new_substitute = Substitute(user=new_user, name=name, email=email, location=location, phone=phone,
                                qualifications=qualifications, verification_id=verification_id)
    db.session.add(new_substitute)
    db.session.commit()

    return jsonify(message=signup_confirmation_message('Substitute'))

# app route to update user for Admin 
@app.route('/update_user_to_substitute/<int:user_id>', methods=['POST'])
def update_user_to_substitute(user_id):
    user = User.query.get(user_id)
    if user:
        user.role = 'Substitute'
        db.session.commit()

        new_substitute = Substitute(
            user_id=user.id,
            qualifications=request.json['qualifications'],
            verification_id=request.json['verification_id']
        )
        db.session.add(new_substitute)
        db.session.commit()

        return jsonify({"message": "User updated to substitute successfully."})
    else:
        return jsonify({"error": "User not found."}), 404

# app route for sign up confirmation 
def signup_confirmation_message(role):
    if role == 'Teacher':
        return "You have successfully signed up as a Teacher!"
    elif role == 'Substitute':
        return "You have successfully signed up as a Substitute!"
    else:
        return "You have successfully signed up!"

# app route to create site admin 
@app.route('/create_site_admin', methods=['GET'])
def create_site_admin():
    email = 'colly@example.com'
    password = 'Disney4Life!'
    name = 'Collen Chase'
    location = 'Aurora, CO'
    phone = '303-867-5309'
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists."})
    user = User(name=name, email=email, location=location, phone=phone, role='SiteAdmin', password=password)
    db.session.add(user)
    site_admin = SiteAdmin(name=name, email=email, phone=phone)
    
    db.session.add(site_admin)
    db.session.commit()
    return jsonify({"message": "SiteAdmin user created successfully."})

# app route for siteadmin to Delete user
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

   
    if user.role == 'Teacher':
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if teacher:
            db.session.delete(teacher)
    elif user.role == 'Substitute':
        substitute = Substitute.query.filter_by(user_id=user_id).first()
        if substitute:
            db.session.delete(substitute)


    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully."})

# app route for log out
@app.route('/logout', methods=['DELETE'])
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5555)