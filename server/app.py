from flask import Flask, jsonify, request, make_response, render_template
from flask_restful import Resource
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from config import app, db, api
from flask_cors import CORS

CORS(app, supports_credentials=True)
app.template_folder = "templates"


class SignUp(Resource):
    def post(self):
        try:
            data = request.get_json()
            # Your logic for creating a new user and saving it to the database goes here
            # Make sure to handle password hashing and error handling
            return make_response({'message': 'New user created successfully'}, 201)
        except:
            return make_response({'errors': ['Validation errors']}, 400)

class CheckSession(Resource):
    def get(self):
        # Your logic for checking the current user session and returning the user data if logged in goes here
        # Make sure to handle the case where no user is currently logged in
        return make_response({'message': 'User session checked successfully'}, 200)

class LogIn(Resource):
    def post(self):
        data = request.get_json()
        # Your logic for authenticating the user login credentials goes here
        # Make sure to handle invalid username and password cases
        # If login is successful, set the user_id in the session
        return make_response({'message': 'Login successful'}, 201)

class LogOut(Resource):
    def delete(self):
        # Your logic for logging out the user (clearing the session) goes here
        # Make sure to handle the case where no user is currently logged in
        return make_response({'message': 'Logged out successfully'}, 204)


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify(users)

class TeacherResource(Resource):
    def get(self):
        teachers = Teacher.query.all()
        return jsonify(teachers)

class SubstituteResource(Resource):
    def get(self):
        substitutes = Substitute.query.all()
        return jsonify(substitutes)

class SiteAdminResource(Resource):
    def get(self):
        site_admins = SiteAdmin.query.all()
        return jsonify(site_admins)

class CourseResource(Resource):
    def get(self):
        courses = Course.query.all()
        return jsonify(courses)

class ReviewResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return jsonify(reviews)
    
api.add_resource(SignUp, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')
api.add_resource(UserResource, '/users')
api.add_resource(TeacherResource, '/teachers')
api.add_resource(SubstituteResource, '/substitutes')
api.add_resource(SiteAdminResource, '/site_admins')
api.add_resource(CourseResource, '/courses')
api.add_resource(ReviewResource, '/reviews')

# Route for teacher form
@app.route('/teacher-form', methods=['GET', 'POST'])
def teacher_form():
    if request.method == 'POST':
        # Get form data and create a new Teacher record in the database
        data = request.form
        teacher = Teacher(
            name=data['name'],
            school=data['school'],
            location=data['location'],
            grade_or_course=data['grade_or_course'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(teacher)
        db.session.commit()
        return make_response({'message': 'Teacher added successfully'}, 201)
    return render_template('teacher_form.html')

# Route for substitute form
@app.route('/substitute-form', methods=['GET', 'POST'])
def substitute_form():
    if request.method == 'POST':
        # Get form data and create a new Substitute record in the database
        data = request.form
        substitute = Substitute(
            name=data['name'],
            verification_id=data['verification_id'],
            location=data['location'],
            grade_or_course=data['grade_or_course'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(substitute)
        db.session.commit()
        return make_response({'message': 'Substitute added successfully'}, 201)
    return render_template('substitute_form.html')

if __name__ == '__main__':
    app.run(port=5555)
