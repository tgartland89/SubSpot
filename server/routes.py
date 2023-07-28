from flask import render_template_string, request, make_response, redirect, url_for
from app import app, db, bcrypt
from models import User, Teacher, Substitute, Course, Review
from sqlalchemy.exc import IntegrityError
from resources import SignUp, LogIn, LogOut, UserResource, TeacherResource, SubstituteResource, SiteAdminResource, CourseResource, ReviewResource, RequestResource

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
    return render_template_string(home_page_content)

@app.route('/teacher-signup', methods=['POST'])
def teacher_signup():
    try:
        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return make_response({'errors': ['Password and Confirm Password do not match']}, 400)

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return make_response({'errors': ['Email already in use']}, 400)

        user = User(
            email=data['email'],
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='Teacher',
        )
        db.session.add(user)
        db.session.commit()

        return make_response({'message': 'Teacher registered successfully'}, 201)

    except IntegrityError as e:
        db.session.rollback()  
        return make_response({'errors': ['Database integrity error']}, 500)
    except Exception as e:
        print(e)
        return make_response({'errors': ['Validation errors']}, 400)

@app.route('/teacher-form', methods=['GET', 'POST'])
def teacher_form():

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.role == 'Teacher':
            if request.method == 'POST':
                return make_response({'message': 'Teacher added successfully'}, 201)
            return make_response({'message': 'Teacher form is available'}, 200)

    return make_response({'errors': ['Unauthorized']}, 401)

@app.route('/substitute-signup', methods=['POST'])
def substitute_signup():
    try:
        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            return make_response({'errors': ['Password and Confirm Password do not match']}, 400)

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return make_response({'errors': ['Email already in use']}, 400)

        user = User(
            email=data['email'],
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='Substitute',
        )
        db.session.add(user)
        db.session.commit()

        return make_response({'message': 'Substitute registered successfully'}, 201)

    except IntegrityError as e:
        db.session.rollback()  
        return make_response({'errors': ['Database integrity error']}, 500)
    except Exception as e:
        print(e)
        return make_response({'errors': ['Validation errors']}, 400)

@app.route('/substitute-form', methods=['GET', 'POST'])
def substitute_form():

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.role == 'Substitute':
            if request.method == 'POST':
                return make_response({'message': 'Substitute added successfully'}, 201)
            return make_response({'message': 'Substitute form is available'}, 200)

    return make_response({'errors': ['Unauthorized']}, 401)

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