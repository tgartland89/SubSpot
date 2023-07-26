from config import app, db, bcrypt
from flask import session, request, make_response, render_template, redirect, url_for
from models import User
from config import app, db

@app.route('/teacher-form', methods=['GET', 'POST'])
def teacher_form():

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.role == 'Teacher':
            if request.method == 'POST':

                return make_response({'message': 'Teacher added successfully'}, 201)
            return render_template('teacher_form.html')

    return make_response({'errors': ['Unauthorized']}, 401)

@app.route('/substitute-form', methods=['GET', 'POST'])
def substitute_form():

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.role == 'Substitute':
            if request.method == 'POST':
  
                return make_response({'message': 'Substitute added successfully'}, 201)
            return render_template('substitute_form.html')

    return make_response({'errors': ['Unauthorized']}, 401)

@app.route('/substitute-signup', methods=['POST'])
def substitute_signup():
    try:
        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            return make_response({'errors': ['Password and Confirm Password do not match']}, 400)

        user = User(
            email=data['email'],
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='Substitute',
        )
        db.session.add(user)
        db.session.commit()

        user_id = user.id

        substitute = Substitute(
            user_id=user_id,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            location=data['location'],
            grade_or_course=data['grade_or_course'],
            verification_id=data['verification_id'],
            qualifications=data['qualifications'],
        )

        db.session.add(substitute)
        db.session.commit()

        return make_response({'message': 'New substitute created successfully'}, 201)
    except Exception as e:
        print(e)
        return make_response({'errors': ['Validation errors']}, 400)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response({'errors': ['User not found']}, 404)

        if not bcrypt.check_password_hash(user.password_hash, password):
            return make_response({'errors': ['Invalid password']}, 401)

        session['user_id'] = user.id

        if user.role == 'Teacher':
            return redirect(url_for('teacher_form'))
        elif user.role == 'Substitute':
            return redirect(url_for('substitute_form'))
        else:
            return make_response({'errors': ['Invalid user role']}, 400)

    return render_template('login.html') 

@app.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return make_response({'message': 'Logged out successfully'}, 204)
    else:
        return make_response({'errors': ['User not logged in']}, 401)