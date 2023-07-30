import os
from flask import Flask, make_response, request, redirect, url_for, session, render_template_string, jsonify
from config import db, bcrypt
from models import User, Teacher, Substitute, SiteAdmin, Review, Request, Course
from flask_migrate import Migrate
from faker import Faker 
from flask_cors import CORS

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            login_page_content = "Invalid email or password. Please try again."
            response = make_response(login_page_content)
            response.headers['Content-Type'] = 'text/html'
            return response

    login_page_content = "Log In"
    response = make_response(login_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/substitute/<int:substitute_id>')
def substitute_info(substitute_id):
    substitute = Substitute.query.get(substitute_id)

    if substitute:
        requests_received = Request.query.filter_by(Substitute_user_id=substitute_id).all()
        substitute_info_content = f"{substitute.name}'s Information:\nName: {substitute.name}\nEmail: {substitute.email}\nLocation: {substitute.location}\nPhone: {substitute.phone}\nQualifications: {substitute.qualifications}\nVerification ID: {substitute.verification_id}"
        return substitute_info_content
    else:
        return "Substitute not found.", 404

@app.route('/request/<int:substitute_id>', methods=['POST'])
def request_substitute(substitute_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    teacher_id = session['user_id']

    new_request = Request(
        Substitute_user_id=substitute_id,
        Teacher_id=session['user_id'],
        Teacher_school="School Name",
        Teacher_school_location="School Location",
        Course_Being_covered="Course Name",
        Confirmation=None,
        Message_sub_sent_to=None,
        Teacher_if_declined=None
    )

    db.session.add(new_request)
    db.session.commit()

    return redirect(url_for('substitute_info', substitute_id=substitute_id))

@app.route('/signup', methods=['GET', 'POST'])
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

            return jsonify({"message": signup_confirmation_message(role)})

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
  

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5555)
