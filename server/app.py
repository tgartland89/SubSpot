import os
from flask import Flask, make_response, request, redirect, url_for, session, render_template_string
from config import db, bcrypt
from models import User, Teacher, Substitute, SiteAdmin, Review, Request, Course
from flask_migrate import Migrate
from faker import Faker 

fake = Faker()

app = Flask(__name__)
migrate = Migrate(app, db) 
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subspot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

@app.route('/')
def home():
    if 'user_id' in session:
        substitutes = Substitute.query.all()
        home_page_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SubSpot - Home</title>
        </head>
        <body>
            <h1>Welcome to SubSpot!</h1>
            <p>Find substitutes quickly for your teaching needs.</p>
            <a href="/logout">Log Out</a>
            <!-- Display the list of substitutes -->
            <h2>Substitutes:</h2>
            <ul>
                %s
            </ul>
        </body>
        </html>
        """ % generate_substitute_list(substitutes)
    else:
        home_page_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SubSpot - Home</title>
        </head>
        <body>
            <h1>Welcome to SubSpot!</h1>
            <p>Find substitutes quickly for your teaching needs.</p>
            <a href="/login">Log In</a><br>
            <a href="/signup">Sign Up</a>
        </body>
        </html>
        """
    response = make_response(home_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

def generate_substitute_list(substitutes):
    list_html = ""
    for substitute in substitutes:
        list_html += "<li><a href='/substitute/{0}'>{1}</a></li>".format(substitute.id, substitute.name)
    return list_html

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
            login_page_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>SubSpot - Log In</title>
            </head>
            <body>
                <h1>Log In</h1>
                <p style="color: red;">Invalid email or password. Please try again.</p>
                <form method="post">
                    <label for="email">Email:</label>
                    <input type="email" name="email" required><br>

                    <label for="password">Password:</label>
                    <input type="password" name="password" required><br>

                    <input type="submit" value="Log In">
                </form>
            </body>
            </html>
            """
            response = make_response(login_page_content)
            response.headers['Content-Type'] = 'text/html'
            return response

    login_page_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SubSpot - Log In</title>
    </head>
    <body>
        <h1>Log In</h1>
        <form method="post">
            <label for="email">Email:</label>
            <input type="email" name="email" required><br>

            <label for="password">Password:</label>
            <input type="password" name="password" required><br>

            <input type="submit" value="Log In">
        </form>
    </body>
    </html>
    """
    response = make_response(login_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/substitute/<int:substitute_id>')
def substitute_info(substitute_id):
    substitute = Substitute.query.get(substitute_id)

    if substitute:
        requests_received = Request.query.filter_by(Substitute_user_id=substitute_id).all()

        substitute_info_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SubSpot - Substitute Information</title>
        </head>
        <body>
            <h1>{{ substitute.name }}'s Information</h1>
            <p><strong>Name:</strong> {{ substitute.name }}</p>
            <p><strong>Email:</strong> {{ substitute.email }}</p>
            <p><strong>Location:</strong> {{ substitute.location }}</p>
            <p><strong>Phone:</strong> {{ substitute.phone }}</p>
            <p><strong>Qualifications:</strong> {{ substitute.qualifications }}</p>
            <p><strong>Verification ID:</strong> {{ substitute.verification_id }}</p>

            <!-- Add the Request button -->
            <form method="post" action="/request/{{ substitute.id }}">
                <input type="submit" value="Request">
            </form>

            <!-- Display the list of requests -->
            <h2>Requests Received:</h2>
            <ul>
                {% for request_data in requests_received %}
                    <li>
                        <strong>Teacher:</strong> {{ request_data.teacher.name }}<br>
                        <strong>School:</strong> {{ request_data.Teacher_school }}<br>
                        <strong>Location:</strong> {{ request_data.Teacher_school_location }}<br>
                        <form method="post" action="/substitute/confirm/{{ request_data.id }}">
                            <input type="submit" value="Confirm">
                        </form>
                        <form method="post" action="/substitute/decline/{{ request_data.id }}">
                            <input type="submit" value="Decline">
                        </form>
                    </li>
                {% endfor %}
            </ul>

            <!-- Link back to the home page -->
            <a href="/">Go Back to Home</a>
        </body>
        </html>
        """
        return render_template_string(substitute_info_content, substitute=substitute, requests_received=requests_received)
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

@app.route('/substitute/request_received/<int:request_id>')
def substitute_request_received(request_id):
    request_data = Request.query.get(request_id)
    if request_data is None:
        return "Request not found.", 404

    substitute = Substitute.query.get(request_data.Substitute_user_id)
    substitute_request_received_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SubSpot - Request Received</title>
    </head>
    <body>
        <h1>Request Received</h1>
        <p>You have received a request from {{ request_data.Teacher_name }}.</p>
        <p>School: {{ request_data.Teacher_school }}</p>
        <p>Location: {{ request_data.Teacher_school_location }}</p>

        <form method="post" action="/substitute/confirm/{{ request_data.id }}">
            <input type="submit" value="Confirm">
        </form>

        <form method="post" action="/substitute/decline/{{ request_data.id }}">
            <input type="submit" value="Decline">
        </form>

        <a href="/">Go Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(substitute_request_received_content, request_data=request_data)


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

            return signup_confirmation_message(role)

        elif role == 'Substitute':
            qualifications = request.form.get('qualifications')
            verification_id = request.form.get('verification_id')

            user = User(name=name, email=email, location=location, phone=phone, role='Substitute', password=password)
            db.session.add(user)
            db.session.commit()

            substitute = Substitute(user_id=user.id, name=name, email=email, location=location, phone=phone, qualifications=qualifications, verification_id=verification_id)
            db.session.add(substitute)
            db.session.commit()

            return signup_confirmation_message(role)

    signup_page_content = """
<!DOCTYPE html>
<html>
<head>
    <title>SubSpot - Sign Up</title>
</head>
<body onload="toggleFormFields()">
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

def signup_confirmation_message(role):
    if role not in ['Teacher', 'Substitute']:
        return redirect(url_for('home'))

    confirmation_page_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SubSpot - Sign Up Confirmation</title>
    </head>
    <body>
        <h1>Sign Up Successful!</h1>
        <p>Congratulations! You have successfully signed up as a {role}.</p>
        <a href="/">Go to Home</a>
    </body>
    </html>
    """
    response = make_response(confirmation_page_content)
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5555)