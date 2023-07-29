import os
from flask import Flask, make_response, request, redirect, url_for
from config import db, bcrypt
from models import User, Teacher, Substitute, SiteAdmin, Review, Request, Course
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db) 
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subspot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

@app.route('/')
def home():
    home_page_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SubSpot - Home</title>
    </head>
    <body>
        <h1>Welcome to SubSpot!</h1>
        <p>Find substitutes quickly for your teaching needs.</p>
        <a href="/login">Log In</a> or <a href="/signup">Sign Up</a>
    </body>
    </html>
    """
    response = make_response(home_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/login')
def login():
    login_page_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SubSpot - Log In</title>
    </head>
    <body>
        <h1>Log In</h1>
        <!-- Add your login form here -->
    </body>
    </html>
    """
    response = make_response(login_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        role = request.form.get('role')

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        location = request.form.get('location')
        phone = request.form.get('phone')

        if password != confirm_password:
            return redirect(url_for('signup'))

        if role == 'Teacher':
            school_name = request.form.get('school_name')
            course_name = request.form.get('course_name')

            user = User(name=name, email=email, location=location, phone=phone, role='Teacher', password=password)
            db.session.add(user)
            db.session.commit()

            teacher = Teacher(user_id=user.id, name=name, email=email, location=location, phone=phone, course_name=course_name)
            db.session.add(teacher)
            db.session.commit()

            return redirect(url_for('home'))

        elif role == 'Substitute':
            qualifications = request.form.get('qualifications')
            verification_id = request.form.get('verification_id')

            user = User(name=name, email=email, location=location, phone=phone, role='Substitute', password=password)
            db.session.add(user)
            db.session.commit()

            substitute = Substitute(user_id=user.id, name=name, email=email, location=location, phone=phone, qualifications=qualifications, verification_id=verification_id)
            db.session.add(substitute)
            db.session.commit()

            return redirect(url_for('home'))

    signup_page_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SubSpot - Sign Up</title>
    </head>
    <body>
        <h1>Sign Up</h1>
        <form method="post" id="signup-form">
            <label for="role">Choose Role:</label>
            <select name="role" id="role" onchange="toggleFormFields()">
                <option value="Teacher">Teacher</option>
                <option value="Substitute">Substitute</option>
            </select>
            <br><br>

            <label for="name">Name:</label>
            <input type="text" name="name" required><br>

            <label for="email">Email:</label>
            <input type="email" name="email" required><br>

            <label for="password">Password:</label>
            <input type="password" name="password" required><br>

            <label for="confirm_password">Confirm Password:</label>
            <input type="password" name="confirm_password" required><br>

            <label for="location">Location:</label>
            <input type="text" name="location" required><br>

            <!-- School Name (Teacher) -->
            <label for="school_name" id="school_name_label" style="display:none">School Name:</label>
            <input type="text" name="school_name" id="school_name_input" style="display:none"><br>

            <!-- Phone -->
            <label for="phone">Phone:</label>
            <input type="text" name="phone" required><br>

            <!-- Course Name (Teacher) -->
            <label for="course_name" id="course_name_label" style="display:none">Course Name:</label>
            <input type="text" name="course_name" id="course_name_input" style="display:none"><br>

            <!-- Qualifications (Substitute) -->
            <label for="qualifications" id="qualifications_label" style="display:none">Qualifications:</label>
            <input type="text" name="qualifications" id="qualifications_input" style="display:none"><br>

            <!-- Verification ID (Substitute) -->
            <label for="verification_id" id="verification_id_label" style="display:none">Verification ID:</label>
            <input type="text" name="verification_id" id="verification_id_input" style="display:none"><br>

            <input type="submit" value="Sign Up">
        </form>

        <script>
            function toggleFormFields() {
                var role = document.getElementById('role').value;

                var schoolNameLabel = document.getElementById('school_name_label');
                var schoolNameInput = document.getElementById('school_name_input');

                var courseNameLabel = document.getElementById('course_name_label');
                var courseNameInput = document.getElementById('course_name_input');

                var qualificationsLabel = document.getElementById('qualifications_label');
                var qualificationsInput = document.getElementById('qualifications_input');

                var verificationIdLabel = document.getElementById('verification_id_label');
                var verificationIdInput = document.getElementById('verification_id_input');

                if (role === 'Teacher') {
                    schoolNameLabel.style.display = 'inline-block';
                    schoolNameInput.style.display = 'inline-block';
                    courseNameLabel.style.display = 'inline-block';
                    courseNameInput.style.display = 'inline-block';

                    qualificationsLabel.style.display = 'none';
                    qualificationsInput.style.display = 'none';
                    verificationIdLabel.style.display = 'none';
                    verificationIdInput.style.display = 'none';
                } else if (role === 'Substitute') {
                    schoolNameLabel.style.display = 'none';
                    schoolNameInput.style.display = 'none';
                    courseNameLabel.style.display = 'none';
                    courseNameInput.style.display = 'none';

                    qualificationsLabel.style.display = 'inline-block';
                    qualificationsInput.style.display = 'inline-block';
                    verificationIdLabel.style.display = 'inline-block';
                    verificationIdInput.style.display = 'inline-block';
                }
            }
        </script>
    </body>
    </html>
    """

    response = make_response(signup_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

if __name__ == '__main__':
    app.run(port=5555)
