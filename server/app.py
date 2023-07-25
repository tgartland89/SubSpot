from flask import Flask, jsonify, request, make_response, render_template
from flask_restful import Resource, fields, marshal 
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from config import app, db, api
from flask_cors import CORS

CORS(app, supports_credentials=True)
app.template_folder = "templates"

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password_hash': fields.String,
    'profile_picture': fields.String,
    'role': fields.String,
}

teacher_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'school': fields.String,
    'location': fields.String,
    'grade_or_course': fields.String,
    'image_url': fields.String,
}

substitute_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'verification_id': fields.String,
    'location': fields.String,
    'grade_or_course': fields.String,
    'qualifications': fields.String,
    'image_url': fields.String,
}

site_admin_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'image_url': fields.String,
}

course_fields = {
    'id': fields.Integer,
    'teacher_id': fields.Integer,
    'substitute_id': fields.Integer,
    'class_subject': fields.String,
    'date': fields.String,
    'time': fields.String,
    'status': fields.String,
}
review_fields = {
    'id': fields.Integer,
    'teacher_id': fields.Integer,
    'substitute_id': fields.Integer,
    'rating': fields.Float,
    'comment': fields.String,
}

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
        serialized_users = [marshal(user, user_fields) for user in users]
        return jsonify(serialized_users)

class TeacherResource(Resource):
    def get(self):
        teachers = Teacher.query.all()
        # Use marshal to serialize the Teacher objects
        serialized_teachers = [marshal(teacher, teacher_fields) for teacher in teachers]
        return jsonify(serialized_teachers)

class SubstituteResource(Resource):
    def get(self):
        substitutes = Substitute.query.all()
        serialized_substitutes = [marshal(substitute, substitute_fields) for substitute in substitutes]
        return jsonify(serialized_substitutes)

class SiteAdminResource(Resource):
    def get(self):
        site_admins = SiteAdmin.query.all()
        serialized_site_admins = [marshal(admin, site_admin_fields) for admin in site_admins]
        return jsonify(serialized_site_admins)

class CourseResource(Resource):
    def get(self):
        courses = Course.query.all()
        serialized_courses = [marshal(course, course_fields) for course in courses]
        return jsonify(serialized_courses)

class ReviewResource(Resource):
    def get(self):
        reviews = Review.query.all()
        serialized_reviews = [marshal(review, review_fields) for review in reviews]
        return jsonify(serialized_reviews)
    
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
