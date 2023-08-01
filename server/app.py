import os
from flask import Flask, make_response, request, redirect, url_for, session, jsonify, g
from config import db, bcrypt
from models import User, Teacher, Substitute, SiteAdmin, Request
from flask_migrate import Migrate
from faker import Faker 
from flask_cors import CORS
from functools import wraps

fake = Faker()

app = Flask(__name__)
migrate = Migrate(app, db) 
CORS(app, supports_credentials=True)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subspot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

@app.route('/')
def home():
    if 'user_id' in session:
        substitutes = Substitute.query.all()
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

        if user and user.authenticate(password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            return jsonify({"role": user.role})

        return jsonify({"error": "Invalid email or password. Please try again."}), 401
    
@app.route('/get_user_role', methods=['GET'])
@login_required
def get_user_role():
    if 'user_id' not in session:
        return jsonify({"role": None})

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user:
        return jsonify({"role": user.role}) 
    else:
        return jsonify({"role": None})
    
@app.route('/auth/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        role = request.json.get('role')
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')
        location = request.json.get('location')
        phone = request.json.get('phone')

        if password != confirm_password:
            return redirect(url_for('signup'))

        if role == 'Teacher':
            school_name = request.json.get('school_name')
            course_name = request.json.get('course_name')

            new_user = User(name=name, email=email, location=location, phone=phone, role=role, password=password)
            db.session.add(new_user)
            db.session.commit()

            new_teacher = Teacher(user=new_user, name=name, email=email, location=location, phone=phone, course_name=course_name)
            db.session.add(new_teacher)
            db.session.commit()

            return jsonify(message=signup_confirmation_message(role))

        elif role == 'Substitute':
            qualifications = request.json.get('qualifications')
            verification_id = request.json.get('verification_id')

            new_user = User(name=name, email=email, location=location, phone=phone, role=role, password=password)
            db.session.add(new_user)
            db.session.commit()

            new_substitute = Substitute(user=new_user, name=name, email=email, location=location, phone=phone,
                                        qualifications=qualifications, verification_id=verification_id)
            db.session.add(new_substitute)
            db.session.commit()

            return jsonify({"message": signup_confirmation_message(role)})

    return "Sign Up Form"

def signup_confirmation_message(role):
    if role == 'Teacher':
        return "You have successfully signed up as a Teacher!"
    elif role == 'Substitute':
        return "You have successfully signed up as a Substitute!"
    else:
        return "You have successfully signed up!"
    
@app.route('/teacher-dashboard', methods=['GET'])
@login_required
def teacher_dashboard():
    if session['user_role'] != 'Teacher':
        return jsonify({"error": "Access denied"})

    substitutes = Substitute.query.all()
    substitute_list = []
    for substitute in substitutes:
        substitute_details = {
            "name": substitute.name,
            "email": substitute.email,
            "location": substitute.location,
            "phone": substitute.phone,
            "qualifications": substitute.qualifications,
            "verification_id": substitute.verification_id,
        }
        substitute_list.append(substitute_details)

    return jsonify({"substitutes": substitute_list})

@app.route('/admin-dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    if session['user_role'] != 'SiteAdmin':
        return jsonify({"error": "Access denied"})
    
    site_admin = SiteAdmin.query.first()
    if not site_admin:
        return jsonify({"error": "No SiteAdmin found."})
    admin_details = site_admin.to_dict()
    return jsonify(admin_details)

@app.route('/substitute-dashboard', methods=['GET'])
@login_required
def substitute_dashboard():
    if session['user_role'] != 'Substitute':
        return jsonify({"error": "Access denied"})

    user_id = session['user_id']
    substitute = Substitute.query.filter_by(user_id=user_id).first()

    if not substitute:
        return jsonify({"error": "Substitute not found."})
    substitute_details = substitute.to_dict()

    return jsonify(substitute_details)

@app.route('/make_request', methods=['POST'])
@login_required
def make_request():
    if session['user_role'] != 'Teacher':
        return jsonify({"error": "Access denied"})

    data = request.json
    substitute_id = data.get('substitute_id')
    
    substitute = Substitute.query.get(substitute_id)
    teacher_id = session['user_id']
    teacher = Teacher.query.get(teacher_id)

    if not substitute or not teacher:
        return jsonify({"error": "Substitute or Teacher not found."})
    
    new_request = Request(
        Substitute_user_id=substitute.id,
        Teacher_id=teacher.id,
        Teacher_school=teacher.school_name,
        Teacher_school_location=teacher.location,
        Course_Being_covered=teacher.course_name,
        Confirmation=None,
        Message_sub_sent_to=substitute.name,
        Teacher_if_declined=None
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Request sent successfully"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5555)