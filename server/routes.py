from config import bcrypt
from flask import session, request, make_response, render_template_string, redirect, url_for, redirect, render_template
from models import User, Teacher, Substitute, Course, Review, Request  
from config import app, db
from sqlalchemy.exc import IntegrityError

@app.route('/home')
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
        <a href="/login">Login</a> or <a href="/signup">Sign Up</a>
    </body>
    </html>
    """
    return home_page_content

@app.route('/signup', methods=['GET'])
def signup_selection():
    # The signup_selection route is responsible for rendering the page where the user can choose their role.
    # This page will contain links to the Teacher Signup and Substitute Signup pages.
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Signup Selection</title>
    </head>
    <body>
        <h1>Choose your role:</h1>
        <a href="/signup/teacher">Teacher Signup</a>
        <a href="/signup/substitute">Substitute Signup</a>
    </body>
    </html>
    """

@app.route('/signup/teacher', methods=['GET', 'POST'])
def teacher_signup():
    # The teacher_signup route is responsible for handling both the rendering of the teacher signup form
    # and the form submission.
    if request.method == 'GET':
        # Render the teacher signup form
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Teacher Signup</title>
        </head>
        <body>
            <h1>Teacher Signup</h1>
            <form action="/teacher-signup" method="post">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="password" name="confirm_password" placeholder="Confirm Password" required>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """

    elif request.method == 'POST':
        # Handle the teacher signup form submission and registration logic
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return make_response({'errors': ['Password and Confirm Password do not match']}, 400)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return make_response({'errors': ['Email already in use']}, 400)

        user = User(
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='Teacher',
        )
        db.session.add(user)
        db.session.commit()

        return make_response({'message': 'Teacher registered successfully'}, 201)

@app.route('/signup/substitute', methods=['GET', 'POST'])
def substitute_signup():
    # The substitute_signup route is responsible for handling both the rendering of the substitute signup form
    # and the form submission.
    if request.method == 'GET':
        # Render the substitute signup form
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Substitute Signup</title>
        </head>
        <body>
            <h1>Substitute Signup</h1>
            <form action="/substitute-signup" method="post">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="password" name="confirm_password" placeholder="Confirm Password" required>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """

    elif request.method == 'POST':
        # Handle the substitute signup form submission and registration logic
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return make_response({'errors': ['Password and Confirm Password do not match']}, 400)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return make_response({'errors': ['Email already in use']}, 400)

        user = User(
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='Substitute',
        )
        db.session.add(user)
        db.session.commit()

        return make_response({'message': 'Substitute registered successfully'}, 201)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return make_response({'errors': ['Unauthorized']}, 401)

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user.role == 'Teacher':
        substitutes = Substitute.query.all()
        substitutes_data = [{'id': sub.id, 'name': sub.name} for sub in substitutes]
        return make_response({'substitutes': substitutes_data}, 200)
    elif user.role == 'Substitute':
        requests_data = [{'id': req.id, 'teacher_name': req.teacher.name} for req in user.substitute.requests]
        return make_response({'requests': requests_data}, 200)
    else:
        return make_response({'errors': ['Invalid user role']}, 400)

@app.route('/substitute/<int:substitute_id>', methods=['GET'])
def substitute(substitute_id):
    if 'user_id' not in session:
        return make_response({'errors': ['Unauthorized']}, 401)

    substitute = Substitute.query.get(substitute_id)
    substitute_data = {
        'id': substitute.id,
        'name': substitute.name,
        'qualifications': substitute.qualifications,
        'reviews': [{'teacher_name': review.teacher.name, 'content': review.content} for review in substitute.reviews]
    }

    return make_response({'substitute': substitute_data}, 200)

@app.route('/request', methods=['POST'])
def create_request():
    if 'user_id' not in session:
        return make_response({'errors': ['Unauthorized']}, 401)

    data = request.get_json()
    substitute_id = data.get('substitute_id')
    teacher_id = session['user_id']

    request = Request(teacher_id=teacher_id, substitute_id=substitute_id)
    db.session.add(request)
    db.session.commit()

    return make_response({'message': 'Request sent successfully'}, 201)

@app.route('/requests/<int:request_id>/respond', methods=['POST'])
def respond_to_request(request_id):
    if 'user_id' not in session:
        return make_response({'errors': ['Unauthorized']}, 401)

    data = request.get_json()
    response = data.get('response')
    reason = data.get('reason')
    substitute_id = session['user_id']

    request = Request.query.filter_by(id=request_id, substitute_id=substitute_id).first()
    if not request:
        return make_response({'errors': ['Request not found']}, 404)

    request.response = response
    request.reason = reason
    db.session.commit()

    return make_response({'message': 'Response sent successfully'}, 200)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response({'errors': ['User not found']}, 404)

        if not bcrypt.check_password_hash(user.password_hash, password):
            return make_response({'errors': ['Invalid password']}, 401)

        session['user_id'] = user.id

        if user.role == 'Teacher':
            return make_response({'message': 'Teacher logged in successfully'}, 200)
        elif user.role == 'Substitute':
            return make_response({'message': 'Substitute logged in successfully'}, 200)
        else:
            return make_response({'errors': ['Invalid user role']}, 400)
    except Exception as e:
        print(e)
        return make_response({'errors': ['Validation errors']}, 400)

@app.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return make_response({'message': 'Logged out successfully'}, 204)
    else:
        return make_response({'errors': ['User not logged in']}, 401)