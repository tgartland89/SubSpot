import os
from flask import Flask, make_response, request, redirect, url_for, session, jsonify, g
from config import db, bcrypt
from models import User, Teacher, Substitute, SiteAdmin, Request
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

def create_user(name, email, location, phone, role, password, profile_picture=None):  
    user = User(name=name, email=email, location=location, phone=phone, role=role, password=password)
    user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user.profile_picture = profile_picture

    return user

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

@app.route('/about')
def about():
    about_content = "SubSpot is a site built by the son of a fourth grade teacher who was looking for alternatives to find substitute teachers quickly and efficiently."
    return about_content

def is_logged_in():
    return 'user_id' in session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return jsonify({"error": "Login required."}), 401
        return f(*args, **kwargs)
    return decorated_function

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
         print (user.id)
         session['user_id'] = user.id
         session['user_role'] = user.role
         if user.role == 'teacher':
              session['teacher_user_id'] = user.id
         return jsonify({"role": user.role})
        return jsonify({"error": "Invalid email or password. Please try again."}), 401
    
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

@app.route('/get_teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    teachers_data = [{"id": teacher.id, "name": teacher.name, "email": teacher.email, "location": teacher.location, "phone": teacher.phone} for teacher in teachers]
    return jsonify({"teachers": teachers_data})

@app.route('/get_substitutes', methods=['GET'])
def get_substitutes():
    substitutes = Substitute.query.all()
    substitutes_data = [{"user_id": substitute.user_id, "name": substitute.name, "email": substitute.email, "location": substitute.location, "phone": substitute.phone, "qualifications": substitute.qualifications, "verification_id": substitute.verification_id} for substitute in substitutes]
    return jsonify({"substitutes": substitutes_data})

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

@app.route('/make_request', methods=['POST'])
@login_required
def make_request():
    if session['user_role'] != 'Teacher':
        return jsonify({"error": "Access denied"})

    data = request.json
    substitute_user_id = data.get('substituteUserId')
    teacher_id = session.get('user_id')  
    print("Teacher ID from session:", teacher_id)

    substitute = Substitute.query.filter_by(id=substitute_user_id).first()

    if not substitute:
         return jsonify({"error": "Substitute not found."}), 404

    teacher = Teacher.query.filter(Teacher.user_id == teacher_id).first()

    if not teacher:
        return jsonify({"error": "Teacher not found."})

    new_request = Request(
        substitute_user_id=substitute.user.id,
        teacher_user_id=teacher.id,
        Course_Being_covered=teacher.course_name,
        Confirmation=None,
        Message_sub_sent_to=substitute.email,
        Teacher_if_declined=None,
        school_name=teacher.school_name,
        Teacher_school_location=teacher.school_location,   
    )

    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Request sent successfully"})

@app.route('/auth/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        role = request.json.get('role')

        if role == 'Teacher':
            return signup_teacher()  
        elif role == 'Substitute':
            return signup_substitute()  

    return "Sign Up Form"

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


def signup_confirmation_message(role):
    if role == 'Teacher':
        return "You have successfully signed up as a Teacher!"
    elif role == 'Substitute':
        return "You have successfully signed up as a Substitute!"
    else:
        return "You have successfully signed up!"
    
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

@app.route('/logout', methods=['DELETE'])
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5555)